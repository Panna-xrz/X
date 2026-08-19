"""联系单路由：委方 / 小组联系人 CRUD。"""

from fastapi import APIRouter, Query, status

from app.api.deps import DbSession
from app.models.contact import ContactType
from app.schemas.common import PageResult
from app.schemas.contact import (
    ContactPersonCreate,
    ContactPersonOut,
    ContactPersonUpdate,
)
from app.services import contact_service

router = APIRouter(prefix="/contacts", tags=["联系单"])


@router.get("", response_model=PageResult[ContactPersonOut])
async def list_contacts(
    db: DbSession,
    project_id: int = Query(..., alias="projectId", description="项目ID"),
    contact_type: ContactType | None = Query(
        None, alias="contactType", description="联系单类型：client委方 / team小组"
    ),
    page: int = Query(1, ge=1, description="页码，从1开始"),
    page_size: int = Query(50, ge=1, le=500, alias="pageSize", description="每页条数"),
) -> PageResult[ContactPersonOut]:
    """分页查询联系人，可按 contactType 过滤。"""
    return await contact_service.list_(
        db,
        project_id=project_id,
        contact_type=contact_type,
        page=page,
        page_size=page_size,
    )


@router.post("", response_model=ContactPersonOut, status_code=status.HTTP_201_CREATED)
async def create_contact(
    payload: ContactPersonCreate, db: DbSession
) -> ContactPersonOut:
    """创建联系人。"""
    contact = await contact_service.create(db, payload)
    return ContactPersonOut.model_validate(contact)


@router.get("/{contact_id}", response_model=ContactPersonOut)
async def get_contact(contact_id: int, db: DbSession) -> ContactPersonOut:
    """获取联系人详情。"""
    contact = await contact_service.get(db, contact_id)
    return ContactPersonOut.model_validate(contact)


@router.put("/{contact_id}", response_model=ContactPersonOut)
async def update_contact(
    contact_id: int, payload: ContactPersonUpdate, db: DbSession
) -> ContactPersonOut:
    """更新联系人：仅更新传入字段。"""
    contact = await contact_service.update(db, contact_id, payload)
    return ContactPersonOut.model_validate(contact)


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: DbSession) -> None:
    """删除联系人。"""
    await contact_service.remove(db, contact_id)
