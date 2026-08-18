"""商务管理模型：Contract 合同 + ContractNode 节点 + BillingRecord 收费记账。"""

import enum
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class ContractType(str, enum.Enum):
    """合同类型：main 主合同 / supplement 补充协议。"""

    MAIN = "main"
    SUPPLEMENT = "supplement"


class BillingType(str, enum.Enum):
    """记账类型：income 收款 / refund 退款。"""

    INCOME = "income"
    REFUND = "refund"


class Contract(Base, TimestampMixin):
    """合同表：一个项目可有多个合同（主合同 + 补充协议）。"""

    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # 关联项目
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True, comment="项目ID"
    )
    # 合同名称
    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="合同名称")
    # 合同类型
    contract_type: Mapped[ContractType] = mapped_column(
        Enum(ContractType), nullable=False, default=ContractType.MAIN, comment="合同类型"
    )
    # 甲方
    party_a: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="甲方")
    # 乙方
    party_b: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="乙方")
    # 合同金额
    amount: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True, comment="合同金额")
    # 签订日期
    sign_date: Mapped[date | None] = mapped_column(Date, nullable=True, comment="签订日期")
    # 合同正文内容
    content_text: Mapped[str | None] = mapped_column(Text, nullable=True, comment="合同正文")
    # 补充协议指向的主合同ID
    parent_contract_id: Mapped[int | None] = mapped_column(
        ForeignKey("contracts.id", ondelete="SET NULL"), nullable=True, comment="主合同ID"
    )

    # 合同节点
    nodes: Mapped[list["ContractNode"]] = relationship(
        back_populates="contract", cascade="all, delete-orphan"
    )
    # 记账记录
    billings: Mapped[list["BillingRecord"]] = relationship(
        back_populates="contract", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Contract {self.name} {self.contract_type.value}>"


class ContractNode(Base, TimestampMixin):
    """合同收费节点：约定阶段性收款节点。"""

    __tablename__ = "contract_nodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # 关联合同
    contract_id: Mapped[int] = mapped_column(
        ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False, index=True, comment="合同ID"
    )
    # 节点名称
    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="节点名称")
    # 节点日期
    node_date: Mapped[date | None] = mapped_column(Date, nullable=True, comment="节点日期")
    # 节点金额
    amount: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True, comment="节点金额")
    # 节点状态：pending / done
    status: Mapped[str] = mapped_column(String(50), default="pending", comment="节点状态")

    contract: Mapped["Contract"] = relationship(back_populates="nodes")

    def __repr__(self) -> str:
        return f"<ContractNode {self.name}>"


class BillingRecord(Base, TimestampMixin):
    """收费记账记录：收款/退款流水。"""

    __tablename__ = "billing_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # 关联合同
    contract_id: Mapped[int] = mapped_column(
        ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False, index=True, comment="合同ID"
    )
    # 记账日期
    billing_date: Mapped[date] = mapped_column(Date, nullable=False, comment="记账日期")
    # 金额
    amount: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False, comment="金额")
    # 记账类型
    type: Mapped[BillingType] = mapped_column(
        Enum(BillingType), nullable=False, default=BillingType.INCOME, comment="记账类型"
    )
    # 备注
    note: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    contract: Mapped["Contract"] = relationship(back_populates="billings")

    def __repr__(self) -> str:
        return f"<BillingRecord {self.type.value} {self.amount}>"
