"""项目信息路由：CRUD + AI 提取扩展信息。"""

from fastapi import APIRouter, Query

from app.api.deps import DbSession
from app.schemas.common import PageResult
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate
from app.services import project_service

router = APIRouter(prefix="/projects", tags=["项目信息"])


@router.get("/", response_model=PageResult[ProjectOut])
async def list_projects(
    db: DbSession,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> PageResult[ProjectOut]:
    """分页查询项目列表。"""
    skip = (page - 1) * page_size
    items = await project_service.list_(db, skip=skip, limit=page_size)
    return PageResult[ProjectOut](
        items=[ProjectOut.model_validate(p) for p in items],
        total=len(items),
        page=page,
        page_size=page_size,
    )


@router.post("/", response_model=ProjectOut)
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
    """更新项目。"""
    project = await project_service.update(db, project_id, payload)
    return ProjectOut.model_validate(project)


@router.post("/{project_id}/ai-extract")
async def ai_extract(project_id: int, db: DbSession) -> dict[str, str]:
    """调用 AI 提取项目扩展信息并写入 ProjectExtra。"""
    return await project_service.ai_extract_info(db, project_id)
