"""商务管理 schema：合同与收费节点，camelCase 契约。"""

from datetime import date

from pydantic import Field

from app.models.contract import ContractType
from app.schemas.common import CamelSchema, TimestampSchema


class ContractBase(CamelSchema):
    """合同基础字段。"""

    name: str = Field(..., max_length=255, description="合同名称")
    # 对外别名为 type（前端契约），ORM 属性为 contract_type
    contract_type: ContractType = Field(ContractType.MAIN, alias="type", description="合同类型")
    code: str = Field("", max_length=100, description="合同编号")
    party_a: str | None = Field(None, max_length=255, description="甲方")
    party_b: str | None = Field(None, max_length=255, description="乙方")
    amount: float | None = Field(None, description="合同金额")
    signed_date: date | None = Field(None, description="签订日期")
    status: str = Field("draft", max_length=50, description="合同状态")
    content_text: str | None = Field(None, description="合同正文")
    remarks: str | None = Field(None, description="备注")
    parent_contract_id: int | None = Field(None, description="主合同ID（补充协议指向主合同）")


class ContractCreate(ContractBase):
    """创建合同请求。"""

    project_id: int = Field(..., description="所属项目ID")


class ContractUpdate(CamelSchema):
    """更新合同请求：所有字段可选，仅更新传入字段。"""

    name: str | None = Field(None, max_length=255)
    contract_type: ContractType | None = Field(None, alias="type")
    code: str | None = Field(None, max_length=100)
    project_id: int | None = None
    party_a: str | None = Field(None, max_length=255)
    party_b: str | None = Field(None, max_length=255)
    amount: float | None = None
    signed_date: date | None = None
    status: str | None = Field(None, max_length=50)
    content_text: str | None = None
    remarks: str | None = None
    parent_contract_id: int | None = None


class ContractOut(ContractBase, TimestampSchema):
    """合同响应。"""

    id: int
    project_id: int


class ContractGenerateResult(CamelSchema):
    """AI 起草合同正文响应。"""

    contract_id: int
    content: str


class ContractRiskItem(CamelSchema):
    """AI 合同审核的单条风险项。"""

    clause: str | None = Field(None, description="风险条款")
    level: str | None = Field(None, description="风险等级：高/中/低")
    suggestion: str | None = Field(None, description="改进建议")


class ContractReviewResult(CamelSchema):
    """AI 合同审核响应：risks 为结构化风险清单，解析失败时回退 raw 文本。"""

    contract_id: int
    risks: list[ContractRiskItem] = Field(default_factory=list)
    raw: str | None = None


class ContractNodeBase(CamelSchema):
    """收费节点基础字段。"""

    name: str = Field(..., max_length=255, description="节点名称")
    ratio: float | None = Field(None, ge=0, le=100, description="占合同金额比例(%)")
    amount: float | None = Field(None, description="节点金额")
    plan_date: date | None = Field(None, description="计划收款日期")
    actual_date: date | None = Field(None, description="实际收款日期")
    status: str = Field("planned", max_length=50, description="节点状态")
    remarks: str | None = Field(None, description="备注")


class ContractNodeCreate(ContractNodeBase):
    """创建收费节点请求。"""

    contract_id: int = Field(..., description="所属合同ID")


class ContractNodeUpdate(CamelSchema):
    """更新收费节点请求：所有字段可选。"""

    name: str | None = Field(None, max_length=255)
    ratio: float | None = Field(None, ge=0, le=100)
    amount: float | None = None
    plan_date: date | None = None
    actual_date: date | None = None
    status: str | None = Field(None, max_length=50)
    remarks: str | None = None


class ContractNodeOut(ContractNodeBase, TimestampSchema):
    """收费节点响应。"""

    id: int
    contract_id: int
