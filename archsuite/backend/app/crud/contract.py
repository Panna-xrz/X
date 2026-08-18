"""Contract 数据访问：CRUDContract 含按项目查询与补充协议查询。"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.contract import Contract, ContractType


class CRUDContract(CRUDBase[Contract]):
    """Contract 的 CRUD 实现。"""

    model = Contract

    async def list_by_project(
        self,
        db: AsyncSession,
        project_id: int,
        contract_type: ContractType | None = None,
    ) -> list[Contract]:
        """按项目查询合同，可选过滤合同类型。"""
        stmt = select(Contract).where(Contract.project_id == project_id)
        if contract_type is not None:
            stmt = stmt.where(Contract.contract_type == contract_type)
        result = await db.execute(stmt.order_by(Contract.id))
        return list(result.scalars().all())

    async def list_supplements(
        self, db: AsyncSession, parent_contract_id: int
    ) -> list[Contract]:
        """查询某主合同下的所有补充协议。"""
        result = await db.execute(
            select(Contract)
            .where(Contract.parent_contract_id == parent_contract_id)
            .order_by(Contract.id)
        )
        return list(result.scalars().all())


# 单例
contract_crud = CRUDContract()
