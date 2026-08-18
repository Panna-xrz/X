"""Pydantic schema 层：对外数据契约。"""

from app.schemas.common import CamelSchema, PageResult, TimestampSchema
from app.schemas.contract import (
    ContractCreate,
    ContractGenerateResult,
    ContractNodeCreate,
    ContractNodeOut,
    ContractNodeUpdate,
    ContractOut,
    ContractReviewResult,
    ContractRiskItem,
    ContractUpdate,
)
from app.schemas.project import (
    AiExtractResult,
    ProjectCreate,
    ProjectExtraOut,
    ProjectExtraResponse,
    ProjectOut,
    ProjectUpdate,
)

__all__ = [
    "CamelSchema",
    "PageResult",
    "TimestampSchema",
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectOut",
    "ProjectExtraOut",
    "ProjectExtraResponse",
    "AiExtractResult",
    "ContractCreate",
    "ContractUpdate",
    "ContractOut",
    "ContractGenerateResult",
    "ContractReviewResult",
    "ContractRiskItem",
    "ContractNodeCreate",
    "ContractNodeUpdate",
    "ContractNodeOut",
]
