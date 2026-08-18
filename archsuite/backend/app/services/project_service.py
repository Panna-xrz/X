"""项目业务服务：编排 CRUD + AI 提取扩展信息。"""

import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.factory import get_provider
from app.ai.prompts.project_info import build_extract_prompt
from app.core.exceptions import NotFoundError
from app.core.logging import logger
from app.crud.project import project_crud
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


async def list_(db: AsyncSession, skip: int = 0, limit: int = 20) -> list[Project]:
    """分页查询项目列表。"""
    return await project_crud.get_multi(db, skip=skip, limit=limit)


async def create(db: AsyncSession, obj_in: ProjectCreate) -> Project:
    """创建项目。"""
    return await project_crud.create(db, obj_in.model_dump())


async def get(db: AsyncSession, project_id: int) -> Project:
    """获取项目详情，不存在抛 NotFoundError。"""
    project = await project_crud.get(db, project_id)
    if project is None:
        raise NotFoundError(message=f"项目 {project_id} 不存在")
    return project


async def update(db: AsyncSession, project_id: int, obj_in: ProjectUpdate) -> Project:
    """更新项目，仅更新非 None 字段。"""
    project = await get(db, project_id)
    update_data = obj_in.model_dump(exclude_unset=True)
    return await project_crud.update(db, project, update_data)


async def ai_extract_info(db: AsyncSession, project_id: int) -> dict[str, str]:
    """调用 AI 从项目基本信息提取扩展字段，写入 ProjectExtra。

    提取字段定义见 prompts/project_info.py，结果以 JSON 解析后逐条写入。
    """
    project = await get(db, project_id)
    # 拼装项目基本信息文本
    project_info = (
        f"项目名称：{project.name}\n"
        f"项目编号：{project.code}\n"
        f"项目地点：{project.location or '未知'}\n"
        f"项目类型：{project.type or '未知'}\n"
        f"建设规模：{project.scale or '未知'}\n"
        f"项目描述：{project.description or '无'}"
    )
    messages = build_extract_prompt(project_info)
    provider = get_provider()
    # 调用 AI 提取
    raw = await provider.chat(messages)
    logger.info("AI 提取项目扩展信息完成，project_id=%s", project_id)

    # 解析 JSON 结果并写入扩展表
    try:
        extracted = json.loads(raw)
    except json.JSONDecodeError:
        # 解析失败则把原始文本存入一个 fallback 键
        logger.warning("AI 返回非 JSON，原文存入 raw 字段")
        extracted = {"raw": raw}

    saved: dict[str, str] = {}
    for key, value in extracted.items():
        if not isinstance(value, (str, int, float)) and value is not None:
            continue
        extra = await project_crud.add_extra(
            db,
            project_id=project_id,
            field_key=key,
            field_value=str(value) if value is not None else None,
            ai_source=provider.name,
        )
        saved[extra.field_key] = extra.field_value or ""
    return saved
