"""收费记账路由：记账记录查询与创建，按 contract_id 过滤。"""

from datetime import date

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from app.api.deps import DbSession
from app.crud.base import CRUDBase
from app.models.contract import BillingRecord, BillingType

router = APIRouter(prefix="/billing", tags=["收费记账"])

# BillingRecord 的 CRUD 实例（路由层内联，演示性）
billing_crud = CRUDBase[BillingRecord]()
billing_crud.model = BillingRecord


class BillingCreate(BaseModel):
    """创建记账记录请求。"""

    contract_id: int = Field(..., description="合同ID")
    billing_date: date = Field(..., description="记账日期")
    amount: float = Field(..., description="金额")
    type: BillingType = Field(BillingType.INCOME, description="记账类型")
    note: str | None = Field(None, description="备注")


@router.get("/")
async def list_billing(
    db: DbSession,
    contract_id: int | None = Query(None, description="按合同过滤"),
    limit: int = Query(100, ge=1, le=500),
) -> list[dict[str, object]]:
    """查询记账记录，可按 contract_id 过滤。"""
    from sqlalchemy import select

    stmt = select(BillingRecord)
    if contract_id is not None:
        stmt = stmt.where(BillingRecord.contract_id == contract_id)
    result = await db.execute(stmt.order_by(BillingRecord.id.desc()).limit(limit))
    records = result.scalars().all()
    return [
        {
            "id": r.id,
            "contract_id": r.contract_id,
            "billing_date": str(r.billing_date) if r.billing_date else None,
            "amount": float(r.amount) if r.amount is not None else None,
            "type": r.type.value,
            "note": r.note,
        }
        for r in records
    ]


@router.post("/")
async def create_billing(payload: BillingCreate, db: DbSession) -> dict[str, object]:
    """创建记账记录。"""
    record = await billing_crud.create(db, payload.model_dump())
    return {
        "id": record.id,
        "contract_id": record.contract_id,
        "amount": float(record.amount) if record.amount is not None else None,
        "type": record.type.value,
    }
