"""项目业务服务：编排 CRUD + AI 提取扩展信息。"""

from pydantic.alias_generators import to_camel
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.factory import get_provider
from app.ai.prompts.project_info import build_extract_prompt
from app.core.exceptions import NotFoundError
from app.core.logging import logger
from app.crud.project import project_crud
from app.models.project import Project
from app.schemas.common import PageResult
from app.schemas.project import (
    AiExtractResult,
    ProjectCreate,
    ProjectExtraOut,
    ProjectExtraResponse,
    ProjectOut,
    ProjectUpdate,
)
from app.utils import parse_json_object

# AI 提取键 → 前端扩展信息字段的语义别名（其余键自动 camelCase）
_EXTRA_KEY_ALIAS = {
    "total_building_area": "buildingArea",
    "floor_area_ratio": "plotRatio",
}


def _extra_key_to_camel(key: str) -> str:
    """扩展字段键转 camelCase，带语义别名映射。"""
    if key in _EXTRA_KEY_ALIAS:
        return _EXTRA_KEY_ALIAS[key]
    return to_camel(key)


async def list_(db: AsyncSession, page: int = 1, page_size: int = 20) -> PageResult[ProjectOut]:
    """分页查询项目列表（total 为全量总数）。"""
    skip = (page - 1) * page_size
    items = await project_crud.get_multi(db, skip=skip, limit=page_size, order_by=Project.id.desc())
    total = await project_crud.count(db)
    return PageResult[ProjectOut](
        items=[ProjectOut.model_validate(p) for p in items],
        total=total,
        page=page,
        page_size=page_size,
    )


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
    """更新项目：仅更新传入字段。"""
    project = await get(db, project_id)
    update_data = obj_in.model_dump(exclude_unset=True)
    return await project_crud.update(db, project, update_data)


async def remove(db: AsyncSession, project_id: int) -> None:
    """删除项目（级联删除扩展信息与合同）。"""
    project = await get(db, project_id)
    await project_crud.remove(db, project)


async def get_extra(db: AsyncSession, project_id: int) -> ProjectExtraResponse:
    """获取项目扩展信息：items 为键值对列表，fields 为 camelCase 键对象。"""
    await get(db, project_id)
    extras = await project_crud.get_extras(db, project_id)
    fields = {_extra_key_to_camel(e.field_key): e.field_value for e in extras}
    return ProjectExtraResponse(
        items=[ProjectExtraOut.model_validate(e) for e in extras],
        fields=fields,
    )


async def ai_extract_info(db: AsyncSession, project_id: int) -> AiExtractResult:
    """调用 AI 从项目基本信息提取扩展字段，upsert 写入 ProjectExtra。

    提取字段定义见 prompts/project_info.py，结果以 JSON 解析后逐条写入；
    解析失败时原文保留在 raw 字段。
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
    raw = await provider.chat(messages)
    logger.info("AI 提取项目扩展信息完成，project_id=%s", project_id)

    parsed = parse_json_object(raw)
    if parsed is None:
        logger.warning("AI 返回非 JSON，原文保留在 raw 字段，project_id=%s", project_id)
        return AiExtractResult(project_id=project_id, fields={}, raw=raw)

    fields: dict[str, str | None] = {}
    for key, value in parsed.items():
        if not isinstance(key, str):
            continue
        if value is not None and not isinstance(value, (str, int, float, bool)):
            continue
        str_value = str(value) if value is not None else None
        await project_crud.upsert_extra(
            db,
            project_id=project_id,
            field_key=key,
            field_value=str_value,
            ai_source=provider.name,
        )
        fields[_extra_key_to_camel(key)] = str_value
    return AiExtractResult(project_id=project_id, fields=fields)
