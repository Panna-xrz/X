"""项目详细信息业务服务：指标 / 场地周边 / 物理环境 / 人文环境 upsert + 建筑单体 CRUD。

1:1 关系（指标/周边/物理/人文）：upsert 语义，同 project_id 存在则更新，否则创建。
建筑单体（1:N）：标准 CRUD，按项目查询列表。
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.crud.project import project_crud
from app.crud.project_detail import (
    project_building_crud,
    project_cultural_crud,
    project_metric_crud,
    project_physical_crud,
    project_surrounding_crud,
)
from app.models.project_detail import ProjectBuilding
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

# ========== 指标信息 ==========

async def upsert_metric(
    db: AsyncSession, project_id: int, payload: ProjectMetricUpsert
) -> ProjectMetricOut:
    """upsert 项目指标信息：1:1 关系，存在则更新，否则创建。"""
    await _ensure_project(db, project_id)
    data = payload.model_dump(exclude={"project_id"})
    metric = await project_metric_crud.upsert(db, project_id, data)
    return ProjectMetricOut.model_validate(metric)


async def get_metric(db: AsyncSession, project_id: int) -> ProjectMetricOut:
    """获取项目指标信息，不存在抛 NotFoundError。"""
    await _ensure_project(db, project_id)
    metric = await project_metric_crud.get_by_project(db, project_id)
    if metric is None:
        raise NotFoundError(message=f"项目 {project_id} 暂无指标信息")
    return ProjectMetricOut.model_validate(metric)


# ========== 场地周边 ==========

async def upsert_surrounding(
    db: AsyncSession, project_id: int, payload: ProjectSurroundingUpsert
) -> ProjectSurroundingOut:
    """upsert 场地周边信息。"""
    await _ensure_project(db, project_id)
    data = payload.model_dump(exclude={"project_id"})
    surrounding = await project_surrounding_crud.upsert(db, project_id, data)
    return ProjectSurroundingOut.model_validate(surrounding)


async def get_surrounding(db: AsyncSession, project_id: int) -> ProjectSurroundingOut:
    """获取场地周边信息，不存在抛 NotFoundError。"""
    await _ensure_project(db, project_id)
    surrounding = await project_surrounding_crud.get_by_project(db, project_id)
    if surrounding is None:
        raise NotFoundError(message=f"项目 {project_id} 暂无场地周边信息")
    return ProjectSurroundingOut.model_validate(surrounding)


# ========== 物理环境 ==========

async def upsert_physical(
    db: AsyncSession, project_id: int, payload: ProjectPhysicalUpsert
) -> ProjectPhysicalOut:
    """upsert 物理环境信息。"""
    await _ensure_project(db, project_id)
    data = payload.model_dump(exclude={"project_id"})
    physical = await project_physical_crud.upsert(db, project_id, data)
    return ProjectPhysicalOut.model_validate(physical)


async def get_physical(db: AsyncSession, project_id: int) -> ProjectPhysicalOut:
    """获取物理环境信息，不存在抛 NotFoundError。"""
    await _ensure_project(db, project_id)
    physical = await project_physical_crud.get_by_project(db, project_id)
    if physical is None:
        raise NotFoundError(message=f"项目 {project_id} 暂无物理环境信息")
    return ProjectPhysicalOut.model_validate(physical)


# ========== 人文环境 ==========

async def upsert_cultural(
    db: AsyncSession, project_id: int, payload: ProjectCulturalUpsert
) -> ProjectCulturalOut:
    """upsert 人文环境信息。"""
    await _ensure_project(db, project_id)
    data = payload.model_dump(exclude={"project_id"})
    cultural = await project_cultural_crud.upsert(db, project_id, data)
    return ProjectCulturalOut.model_validate(cultural)


async def get_cultural(db: AsyncSession, project_id: int) -> ProjectCulturalOut:
    """获取人文环境信息，不存在抛 NotFoundError。"""
    await _ensure_project(db, project_id)
    cultural = await project_cultural_crud.get_by_project(db, project_id)
    if cultural is None:
        raise NotFoundError(message=f"项目 {project_id} 暂无人文环境信息")
    return ProjectCulturalOut.model_validate(cultural)


# ========== 建筑单体 ==========

async def list_buildings(
    db: AsyncSession, project_id: int
) -> list[ProjectBuildingOut]:
    """查询项目全部建筑单体（按 id 升序）。"""
    await _ensure_project(db, project_id)
    buildings = await project_building_crud.list_by_project(db, project_id)
    return [ProjectBuildingOut.model_validate(b) for b in buildings]


async def create_building(
    db: AsyncSession, payload: ProjectBuildingCreate
) -> ProjectBuildingOut:
    """创建建筑单体：校验所属项目存在。"""
    await _ensure_project(db, payload.project_id)
    building = await project_building_crud.create(db, payload.model_dump())
    return ProjectBuildingOut.model_validate(building)


async def get_building(db: AsyncSession, building_id: int) -> ProjectBuilding:
    """获取建筑单体，不存在抛 NotFoundError。"""
    building = await project_building_crud.get(db, building_id)
    if building is None:
        raise NotFoundError(message=f"建筑单体 {building_id} 不存在")
    return building


async def update_building(
    db: AsyncSession, building_id: int, payload: ProjectBuildingUpdate
) -> ProjectBuildingOut:
    """更新建筑单体：仅更新传入字段。"""
    building = await get_building(db, building_id)
    update_data = payload.model_dump(exclude_unset=True)
    updated = await project_building_crud.update(db, building, update_data)
    return ProjectBuildingOut.model_validate(updated)


async def remove_building(db: AsyncSession, building_id: int) -> None:
    """删除建筑单体。"""
    building = await get_building(db, building_id)
    await project_building_crud.remove(db, building)


# ========== 辅助 ==========

async def _ensure_project(db: AsyncSession, project_id: int) -> None:
    """校验项目存在，不存在抛 NotFoundError。"""
    project = await project_crud.get(db, project_id)
    if project is None:
        raise NotFoundError(message=f"项目 {project_id} 不存在")
