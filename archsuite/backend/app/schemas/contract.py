"""商务管理 schema：合同、节点、记账。"""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.models.contract import BillingType, ContractType
from app.schemas.common import TimestampSchema


class ContractBase(BaseModel):
    """合同基础字段。"""

    name: str = Field(..., max_length=255, description="合同名称")
    contract_type: ContractType = Field(ContractType.MAIN, description="合同类型")
    party_a: str | None = Field(None, max_length=255, description="甲方")
    party_b: str | None = Field(None, max_length=255, description="乙方")
    amount: float | None = Field(None, description="合同金额")
    sign_date: date | None = Field(None, description="签订日期")
    content_text: str | None = Field(None, description="合同正文")
    parent_contract_id: int | None = Field(None, description="主合同ID（补充协议指向主合同）")


class ContractCreate(ContractBase):
    """创建合同请求。"""

    project_id: int = Field(..., description="所属项目ID")

    model_config = ConfigDict(from_attributes=True)


class ContractOut(ContractBase, TimestampSchema):
    """合同响应。"""

    id: int
    project_id: int


class ContractNodeOut(BaseModel):
    """合同节点响应。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    contract_id: int
    name: str
    node_date: date | None
    amount: float | None
    status: str


class BillingRecordOut(BaseModel):
    """记账记录响应。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    contract_id: int
    billing_date: date
    amount: float
    type: BillingType
    note: str | None
