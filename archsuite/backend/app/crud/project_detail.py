"""项目详细信息数据访问：指标 / 场地周边 / 物理环境 / 人文环境 / 建筑单体。

1:1 关系表提供 get_by_project 与 upsert；建筑单体（1:N）提供 list_by_project。
"""

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.project_detail import (
    ProjectBuilding,
    ProjectCultural,
    ProjectMetric,
    ProjectPhysical,
    ProjectSurrounding,
)


class ProjectMetricCrud(CRUDBase[ProjectMetric]):
    """项目指标 CRUD：1:1 关系，upsert 语义。"""

    model = ProjectMetric

    async def get_by_project(
        self, db: AsyncSession, project_id: int
    ) -> ProjectMetric | None:
        """按 project_id 查询指标信息（1:1 唯一）。"""
        result = await db.execute(
            select(ProjectMetric).where(ProjectMetric.project_id == project_id)
        )
        return result.scalar_one_or_none()

    async def upsert(
        self, db: AsyncSession, project_id: int, obj_in: dict[str, Any]
    ) -> ProjectMetric:
        """同 project_id 存在则更新，否则创建（避免重复提取产生脏数据）。"""
        result = await db.execute(
            select(ProjectMetric).where(ProjectMetric.project_id == project_id)
        )
        metric = result.scalar_one_or_none()
        if metric is not None:
            for field, value in obj_in.items():
                setattr(metric, field, value)
            await db.commit()
            await db.refresh(metric)
            return metric
        metric = ProjectMetric(project_id=project_id, **obj_in)
        db.add(metric)
        await db.commit()
        await db.refresh(metric)
        return metric


class ProjectSurroundingCrud(CRUDBase[ProjectSurrounding]):
    """场地周边 CRUD：1:1 关系，upsert 语义。"""

    model = ProjectSurrounding

    async def get_by_project(
        self, db: AsyncSession, project_id: int
    ) -> ProjectSurrounding | None:
        """按 project_id 查询场地周边（1:1 唯一）。"""
        result = await db.execute(
            select(ProjectSurrounding).where(
                ProjectSurrounding.project_id == project_id
            )
        )
        return result.scalar_one_or_none()

    async def upsert(
        self, db: AsyncSession, project_id: int, obj_in: dict[str, Any]
    ) -> ProjectSurrounding:
        """同 project_id 存在则更新，否则创建。"""
        result = await db.execute(
            select(ProjectSurrounding).where(
                ProjectSurrounding.project_id == project_id
            )
        )
        surrounding = result.scalar_one_or_none()
        if surrounding is not None:
            for field, value in obj_in.items():
                setattr(surrounding, field, value)
            await db.commit()
            await db.refresh(surrounding)
            return surrounding
        surrounding = ProjectSurrounding(project_id=project_id, **obj_in)
        db.add(surrounding)
        await db.commit()
        await db.refresh(surrounding)
        return surrounding


class ProjectPhysicalCrud(CRUDBase[ProjectPhysical]):
    """物理环境 CRUD：1:1 关系，upsert 语义。"""

    model = ProjectPhysical

    async def get_by_project(
        self, db: AsyncSession, project_id: int
    ) -> ProjectPhysical | None:
        """按 project_id 查询物理环境（1:1 唯一）。"""
        result = await db.execute(
            select(ProjectPhysical).where(ProjectPhysical.project_id == project_id)
        )
        return result.scalar_one_or_none()

    async def upsert(
        self, db: AsyncSession, project_id: int, obj_in: dict[str, Any]
    ) -> ProjectPhysical:
        """同 project_id 存在则更新，否则创建。"""
        result = await db.execute(
            select(ProjectPhysical).where(ProjectPhysical.project_id == project_id)
        )
        physical = result.scalar_one_or_none()
        if physical is not None:
            for field, value in obj_in.items():
                setattr(physical, field, value)
            await db.commit()
            await db.refresh(physical)
            return physical
        physical = ProjectPhysical(project_id=project_id, **obj_in)
        db.add(physical)
        await db.commit()
        await db.refresh(physical)
        return physical


class ProjectCulturalCrud(CRUDBase[ProjectCultural]):
    """人文环境 CRUD：1:1 关系，upsert 语义。"""

    model = ProjectCultural

    async def get_by_project(
        self, db: AsyncSession, project_id: int
    ) -> ProjectCultural | None:
        """按 project_id 查询人文环境（1:1 唯一）。"""
        result = await db.execute(
            select(ProjectCultural).where(ProjectCultural.project_id == project_id)
        )
        return result.scalar_one_or_none()

    async def upsert(
        self, db: AsyncSession, project_id: int, obj_in: dict[str, Any]
    ) -> ProjectCultural:
        """同 project_id 存在则更新，否则创建。"""
        result = await db.execute(
            select(ProjectCultural).where(ProjectCultural.project_id == project_id)
        )
        cultural = result.scalar_one_or_none()
        if cultural is not None:
            for field, value in obj_in.items():
                setattr(cultural, field, value)
            await db.commit()
            await db.refresh(cultural)
            return cultural
        cultural = ProjectCultural(project_id=project_id, **obj_in)
        db.add(cultural)
        await db.commit()
        await db.refresh(cultural)
        return cultural


class ProjectBuildingCrud(CRUDBase[ProjectBuilding]):
    """建筑单体 CRUD：1:N 关系，按项目查询列表。"""

    model = ProjectBuilding

    async def list_by_project(
        self, db: AsyncSession, project_id: int
    ) -> list[ProjectBuilding]:
        """按项目查询全部建筑单体（按 id 升序）。"""
        result = await db.execute(
            select(ProjectBuilding)
            .where(ProjectBuilding.project_id == project_id)
            .order_by(ProjectBuilding.id)
        )
        return list(result.scalars().all())


# 单例
project_metric_crud = ProjectMetricCrud()
project_surrounding_crud = ProjectSurroundingCrud()
project_physical_crud = ProjectPhysicalCrud()
project_cultural_crud = ProjectCulturalCrud()
project_building_crud = ProjectBuildingCrud()
