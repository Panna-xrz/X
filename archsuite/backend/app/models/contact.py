"""联系单模型：委方联系单 + 小组联系单。"""

import enum

from sqlalchemy import Enum as SAEnum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class ContactType(str, enum.Enum):
    """联系单类型：client 委方 / team 小组。"""

    CLIENT = "client"
    TEAM = "team"


class ContactPerson(Base, TimestampMixin):
    """联系单：委方甲方联系人或项目小组成员。

    委方：职务 + 姓名 + 电话
    小组：姓名 + 专业 + 电话
    统一用 role 字段表示「职务」或「专业」，通过 contact_type 区分语义。
    """

    __tablename__ = "contact_persons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # 关联项目
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True, comment="项目ID"
    )
    # 联系单类型
    contact_type: Mapped[ContactType] = mapped_column(
        SAEnum(ContactType, values_callable=lambda e: [m.value for m in e]),
        nullable=False,
        default=ContactType.CLIENT,
        comment="联系单类型：client委方 / team小组",
    )
    # 姓名
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="姓名")
    # 职务（委方）或专业（小组）
    role: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="职务/专业")
    # 电话
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="电话")
    # 备注
    remarks: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="备注")

    project: Mapped["Project"] = relationship(  # noqa: F821
        back_populates="contacts"
    )

    def __repr__(self) -> str:
        return f"<ContactPerson {self.contact_type.value} {self.name}>"
