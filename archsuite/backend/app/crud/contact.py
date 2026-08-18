"""联系单数据访问：委方 / 小组联系人，按项目查询，可按 contact_type 过滤。"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.contact import ContactPerson, ContactType


class ContactPersonCrud(CRUDBase[ContactPerson]):
    """联系人 CRUD。"""

    model = ContactPerson

    async def list_by_project(
        self,
        db: AsyncSession,
        project_id: int,
        contact_type: ContactType | None = None,
    ) -> list[ContactPerson]:
        """按项目查询联系人，可选过滤联系单类型（按 id 升序）。"""
        stmt = select(ContactPerson).where(ContactPerson.project_id == project_id)
        if contact_type is not None:
            stmt = stmt.where(ContactPerson.contact_type == contact_type)
        result = await db.execute(stmt.order_by(ContactPerson.id))
        return list(result.scalars().all())


# 单例
contact_crud = ContactPersonCrud()
