"""商务管理模型：Contract 合同 + ContractNode 收费节点。"""

import enum
from datetime import date

from sqlalchemy import Date, Enum as SAEnum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class ContractType(str, enum.Enum):
    """合同类型：main 主合同 / supplement 补充协议。"""

    MAIN = "main"
    SUPPLEMENT = "supplement"


class Contract(Base, TimestampMixin):
    """合同表：一个项目可有多个合同（主合同 + 补充协议）。"""

    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # 关联项目
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True, comment="项目ID"
    )
    # 合同编号
    code: Mapped[str] = mapped_column(String(100), nullable=False, default="", index=True, comment="合同编号")
    # 合同名称
    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="合同名称")
    # 合同类型（按枚举值 main/supplement 存储，与前端契约一致）
    contract_type: Mapped[ContractType] = mapped_column(
        SAEnum(ContractType, values_callable=lambda e: [m.value for m in e]),
        nullable=False,
        default=ContractType.MAIN,
        comment="合同类型",
    )
    # 甲方
    party_a: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="甲方")
    # 乙方
    party_b: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="乙方")
    # 合同金额
    amount: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True, comment="合同金额")
    # 签订日期
    signed_date: Mapped[date | None] = mapped_column(Date, nullable=True, comment="签订日期")
    # 合同状态：draft/reviewing/signed/terminated
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="draft", server_default="draft", comment="合同状态"
    )
    # 合同正文内容
    content_text: Mapped[str | None] = mapped_column(Text, nullable=True, comment="合同正文")
    # 备注
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")
    # 补充协议指向的主合同ID
    parent_contract_id: Mapped[int | None] = mapped_column(
        ForeignKey("contracts.id", ondelete="SET NULL"), nullable=True, comment="主合同ID"
    )

    project: Mapped["Project"] = relationship(back_populates="contracts")  # noqa: F821
    # 收费节点
    nodes: Mapped[list["ContractNode"]] = relationship(
        back_populates="contract", cascade="all, delete-orphan"
    )
    # 补充协议
    supplements: Mapped[list["Contract"]] = relationship(
        back_populates="parent_contract",
        foreign_keys="Contract.parent_contract_id",
        cascade="all, delete-orphan",
    )
    parent_contract: Mapped["Contract | None"] = relationship(
        back_populates="supplements", remote_side="Contract.id", foreign_keys="Contract.parent_contract_id"
    )

    def __repr__(self) -> str:
        return f"<Contract {self.name} {self.contract_type.value}>"


class ContractNode(Base, TimestampMixin):
    """合同收费节点：约定阶段性收款节点及其计划/实际执行情况。"""

    __tablename__ = "contract_nodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # 关联合同
    contract_id: Mapped[int] = mapped_column(
        ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False, index=True, comment="合同ID"
    )
    # 节点名称（如：设计费-首付款）
    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="节点名称")
    # 占合同金额比例（0-100，单位 %）
    ratio: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="占合同金额比例(%)")
    # 节点金额
    amount: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True, comment="节点金额")
    # 计划收款日期
    plan_date: Mapped[date | None] = mapped_column(Date, nullable=True, comment="计划收款日期")
    # 实际收款日期
    actual_date: Mapped[date | None] = mapped_column(Date, nullable=True, comment="实际收款日期")
    # 节点状态：planned/invoiced/received/overdue
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="planned", server_default="planned", comment="节点状态"
    )
    # 备注
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    contract: Mapped["Contract"] = relationship(back_populates="nodes")

    def __repr__(self) -> str:
        return f"<ContractNode {self.name}>"
