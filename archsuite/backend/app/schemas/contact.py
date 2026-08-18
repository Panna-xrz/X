"""联系单 schema：委方 / 小组联系人，camelCase 契约。"""

from pydantic import Field

from app.models.contact import ContactType
from app.schemas.common import CamelSchema, TimestampSchema
from sqlalchemy import Enum as SAEnum  # noqa: F401 — 仅为类型注解一致性


class ContactPersonBase(CamelSchema):
    """联系人基础字段。"""

    # 对外别名为 contactType（前端契约），ORM 属性为 contact_type
    contact_type: ContactType = Field(
        ContactType.CLIENT, alias="contactType", description="联系单类型：client委方 / team小组"
    )
    name: str = Field(..., max_length=100, description="姓名")
    role: str | None = Field(None, max_length=255, description="职务/专业")
    phone: str | None = Field(None, max_length=50, description="电话")
    remarks: str | None = Field(None, max_length=500, description="备注")


class ContactPersonCreate(ContactPersonBase):
    """创建联系人请求。"""

    project_id: int = Field(..., alias="projectId", description="项目ID")


class ContactPersonUpdate(CamelSchema):
    """更新联系人请求：所有字段可选。"""

    contact_type: ContactType | None = Field(None, alias="contactType")
    name: str | None = Field(None, max_length=100)
    role: str | None = Field(None, max_length=255)
    phone: str | None = Field(None, max_length=50)
    remarks: str | None = Field(None, max_length=500)


class ContactPersonOut(ContactPersonBase, TimestampSchema):
    """联系人响应。"""

    id: int
    project_id: int
