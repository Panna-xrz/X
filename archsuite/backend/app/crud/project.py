"""Project 数据访问：CRUDProject 含扩展信息操作。"""

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.project import Project, ProjectExtra


class CRUDProject(CRUDBase[Project]):
    """Project 的 CRUD 实现，扩展多表存储的 extras 操作。"""

    model = Project

    async def get_extras(self, db: AsyncSession, project_id: int) -> list[ProjectExtra]:
        """获取项目的所有扩展信息。"""
        result = await db.execute(
            select(ProjectExtra)
            .where(ProjectExtra.project_id == project_id)
            .order_by(ProjectExtra.id)
        )
        return list(result.scalars().all())

    async def add_extra(
        self,
        db: AsyncSession,
        project_id: int,
        field_key: str,
        field_value: str | None,
        ai_source: str | None = None,
    ) -> ProjectExtra:
        """新增一条扩展信息。"""
        extra = ProjectExtra(
            project_id=project_id,
            field_key=field_key,
            field_value=field_value,
            ai_source=ai_source,
        )
        db.add(extra)
        await db.commit()
        await db.refresh(extra)
        return extra


# 单例
project_crud = CRUDProject()
