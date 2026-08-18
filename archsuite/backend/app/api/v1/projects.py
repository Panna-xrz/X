"""项目信息路由：CRUD + 扩展信息 + AI 提取。"""

from fastapi import APIRouter, Query, status

from app.api.deps import DbSession
from app.schemas.common import PageResult
from app.schemas.project import (
    AiExtractResult,
    ProjectCreate,
    ProjectExtraResponse,
    ProjectOut,
    ProjectUpdate,
)
from app.services import project_service

router = APIRouter(prefix="/projects", tags=["项目信息"])


@router.get("/", response_model=PageResult[ProjectOut])
async def list_projects(
    db: DbSession,
    page: int = Query(1, ge=1, description="页码，从1开始"),
    page_size: int = Query(20, ge=1, le=100, alias="pageSize", description="每页条数"),
) -> PageResult[ProjectOut]:
    """分页查询项目列表（输出 list/total/page/pageSize）。"""
    return await project_service.list_(db, page=page, page_size=page_size)


@router.post("/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
async def create_project(payload: ProjectCreate, db: DbSession) -> ProjectOut:
    """创建项目。"""
    project = await project_service.create(db, payload)
    return ProjectOut.model_validate(project)


@router.get("/{project_id}", response_model=ProjectOut)
async def get_project(project_id: int, db: DbSession) -> ProjectOut:
    """获取项目详情。"""
    project = await project_service.get(db, project_id)
    return ProjectOut.model_validate(project)


@router.put("/{project_id}", response_model=ProjectOut)
async def update_project(
    project_id: int, payload: ProjectUpdate, db: DbSession
) -> ProjectOut:
    """更新项目：仅更新传入字段。"""
    project = await project_service.update(db, project_id, payload)
    return ProjectOut.model_validate(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, db: DbSession) -> None:
    """删除项目（级联删除扩展信息与合同）。"""
    await project_service.remove(db, project_id)


@router.get("/{project_id}/extra", response_model=ProjectExtraResponse)
async def get_project_extra(project_id: int, db: DbSession) -> ProjectExtraResponse:
    """获取项目扩展信息（items 键值对列表 + fields 结构化对象）。"""
    return await project_service.get_extra(db, project_id)


@router.post("/{project_id}/ai-extract", response_model=AiExtractResult)
async def ai_extract(project_id: int, db: DbSession) -> AiExtractResult:
    """调用 AI 提取项目扩展信息并写入 ProjectExtra。"""
    return await project_service.ai_extract_info(db, project_id)
