"""项目信息路由：CRUD + 扩展信息 + AI 提取 + 项目详细信息子项。"""

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
from app.schemas.project_detail import (
    ProjectBuildingCreate,
    ProjectBuildingOut,
    ProjectBuildingUpdate,
    ProjectCulturalOut,
    ProjectCulturalUpsert,
    ProjectMetricOut,
    ProjectMetricUpsert,
    ProjectPhysicalOut,
    ProjectPhysicalUpsert,
    ProjectSurroundingOut,
    ProjectSurroundingUpsert,
)
from app.services import project_detail_service, project_service

router = APIRouter(prefix="/projects", tags=["项目信息"])


@router.get("", response_model=PageResult[ProjectOut])
async def list_projects(
    db: DbSession,
    page: int = Query(1, ge=1, description="页码，从1开始"),
    page_size: int = Query(50, ge=1, le=500, alias="pageSize", description="每页条数"),
) -> PageResult[ProjectOut]:
    """分页查询项目列表（输出 list/total/page/pageSize）。"""
    return await project_service.list_(db, page=page, page_size=page_size)


@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
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


# ========== 项目详细信息子项 ==========


# ----- 指标信息 -----

@router.get("/{project_id}/metric", response_model=ProjectMetricOut)
async def get_project_metric(project_id: int, db: DbSession) -> ProjectMetricOut:
    """获取项目指标信息。"""
    return await project_detail_service.get_metric(db, project_id)


@router.put("/{project_id}/metric", response_model=ProjectMetricOut)
async def upsert_project_metric(
    project_id: int, payload: ProjectMetricUpsert, db: DbSession
) -> ProjectMetricOut:
    """upsert 项目指标信息（1:1 关系，存在则更新，否则创建）。"""
    return await project_detail_service.upsert_metric(db, project_id, payload)


# ----- 场地周边 -----

@router.get("/{project_id}/surrounding", response_model=ProjectSurroundingOut)
async def get_project_surrounding(
    project_id: int, db: DbSession
) -> ProjectSurroundingOut:
    """获取场地周边信息。"""
    return await project_detail_service.get_surrounding(db, project_id)


@router.put("/{project_id}/surrounding", response_model=ProjectSurroundingOut)
async def upsert_project_surrounding(
    project_id: int, payload: ProjectSurroundingUpsert, db: DbSession
) -> ProjectSurroundingOut:
    """upsert 场地周边信息。"""
    return await project_detail_service.upsert_surrounding(db, project_id, payload)


# ----- 物理环境 -----

@router.get("/{project_id}/physical", response_model=ProjectPhysicalOut)
async def get_project_physical(
    project_id: int, db: DbSession
) -> ProjectPhysicalOut:
    """获取物理环境信息。"""
    return await project_detail_service.get_physical(db, project_id)


@router.put("/{project_id}/physical", response_model=ProjectPhysicalOut)
async def upsert_project_physical(
    project_id: int, payload: ProjectPhysicalUpsert, db: DbSession
) -> ProjectPhysicalOut:
    """upsert 物理环境信息。"""
    return await project_detail_service.upsert_physical(db, project_id, payload)


# ----- 人文环境 -----

@router.get("/{project_id}/cultural", response_model=ProjectCulturalOut)
async def get_project_cultural(
    project_id: int, db: DbSession
) -> ProjectCulturalOut:
    """获取人文环境信息。"""
    return await project_detail_service.get_cultural(db, project_id)


@router.put("/{project_id}/cultural", response_model=ProjectCulturalOut)
async def upsert_project_cultural(
    project_id: int, payload: ProjectCulturalUpsert, db: DbSession
) -> ProjectCulturalOut:
    """upsert 人文环境信息。"""
    return await project_detail_service.upsert_cultural(db, project_id, payload)


# ----- 建筑单体 -----

@router.get("/{project_id}/buildings", response_model=list[ProjectBuildingOut])
async def list_project_buildings(
    project_id: int, db: DbSession
) -> list[ProjectBuildingOut]:
    """查询项目的全部建筑单体（按 id 升序）。"""
    return await project_detail_service.list_buildings(db, project_id)


@router.post(
    "/{project_id}/buildings",
    response_model=ProjectBuildingOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_project_building(
    project_id: int, payload: ProjectBuildingCreate, db: DbSession
) -> ProjectBuildingOut:
    """创建建筑单体。"""
    # URL 的 project_id 优先，覆盖 payload 中的值
    payload = payload.model_copy(update={"project_id": project_id})
    return await project_detail_service.create_building(db, payload)


@router.get(
    "/{project_id}/buildings/{building_id}", response_model=ProjectBuildingOut
)
async def get_project_building(
    project_id: int, building_id: int, db: DbSession
) -> ProjectBuildingOut:
    """获取建筑单体详情。"""
    return ProjectBuildingOut.model_validate(
        await project_detail_service.get_building(db, building_id)
    )


@router.put(
    "/{project_id}/buildings/{building_id}", response_model=ProjectBuildingOut
)
async def update_project_building(
    project_id: int,
    building_id: int,
    payload: ProjectBuildingUpdate,
    db: DbSession,
) -> ProjectBuildingOut:
    """更新建筑单体：仅更新传入字段。"""
    return await project_detail_service.update_building(db, building_id, payload)


@router.delete(
    "/{project_id}/buildings/{building_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project_building(
    project_id: int, building_id: int, db: DbSession
) -> None:
    """删除建筑单体。"""
    await project_detail_service.remove_building(db, building_id)
