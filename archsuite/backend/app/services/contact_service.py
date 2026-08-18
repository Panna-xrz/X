"""联系单业务服务：委方 / 小组联系人 CRUD。

list_ 分页查询（可按 contact_type 过滤），create/get/update/remove 标准 CRUD。
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.crud.contact import contact_crud
from app.crud.project import project_crud
from app.models.contact import ContactPerson, ContactType
from app.schemas.common import PageResult
from app.schemas.contact import (
    ContactPersonCreate,
    ContactPersonOut,
    ContactPersonUpdate,
)


async def list_(
    db: AsyncSession,
    project_id: int,
    contact_type: ContactType | None = None,
    page: int = 1,
    page_size: int = 20,
) -> PageResult[ContactPersonOut]:
    """分页查询联系人，可按 contact_type 过滤（total 为过滤后总数）。"""
    await _ensure_project(db, project_id)
    filters: list = [ContactPerson.project_id == project_id]
    if contact_type is not None:
        filters.append(ContactPerson.contact_type == contact_type)
    skip = (page - 1) * page_size
    items = await contact_crud.get_multi(
        db, skip=skip, limit=page_size, filters=filters, order_by=ContactPerson.id.desc()
    )
    total = await contact_crud.count(db, filters)
    return PageResult[ContactPersonOut](
        items=[ContactPersonOut.model_validate(c) for c in items],
        total=total,
        page=page,
        page_size=page_size,
    )


async def create(db: AsyncSession, payload: ContactPersonCreate) -> ContactPerson:
    """创建联系人：校验所属项目存在。"""
    await _ensure_project(db, payload.project_id)
    return await contact_crud.create(db, payload.model_dump())


async def get(db: AsyncSession, contact_id: int) -> ContactPerson:
    """获取联系人，不存在抛 NotFoundError。"""
    contact = await contact_crud.get(db, contact_id)
    if contact is None:
        raise NotFoundError(message=f"联系人 {contact_id} 不存在")
    return contact


async def update(
    db: AsyncSession, contact_id: int, payload: ContactPersonUpdate
) -> ContactPerson:
    """更新联系人：仅更新传入字段。"""
    contact = await get(db, contact_id)
    update_data = payload.model_dump(exclude_unset=True)
    return await contact_crud.update(db, contact, update_data)


async def remove(db: AsyncSession, contact_id: int) -> None:
    """删除联系人。"""
    contact = await get(db, contact_id)
    await contact_crud.remove(db, contact)


async def _ensure_project(db: AsyncSession, project_id: int) -> None:
    """校验项目存在，不存在抛 NotFoundError。"""
    project = await project_crud.get(db, project_id)
    if project is None:
        raise NotFoundError(message=f"项目 {project_id} 不存在")
