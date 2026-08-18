"""Project 数据访问：项目与扩展信息（upsert 语义）。"""

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

    async def upsert_extra(
        self,
        db: AsyncSession,
        project_id: int,
        field_key: str,
        field_value: str | None,
        ai_source: str | None = None,
    ) -> ProjectExtra:
        """写入一条扩展信息：同键存在则更新，否则新增（避免重复提取产生脏数据）。"""
        result = await db.execute(
            select(ProjectExtra).where(
                ProjectExtra.project_id == project_id,
                ProjectExtra.field_key == field_key,
            )
        )
        extra = result.scalar_one_or_none()
        if extra is not None:
            extra.field_value = field_value
            extra.ai_source = ai_source
            await db.commit()
            await db.refresh(extra)
            return extra
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
