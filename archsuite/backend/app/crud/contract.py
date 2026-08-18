"""Contract 数据访问：合同与收费节点。"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.contract import Contract, ContractNode, ContractType


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


class CRUDContractNode(CRUDBase[ContractNode]):
    """ContractNode（收费节点）的 CRUD 实现。"""

    model = ContractNode

    async def list_by_contract(self, db: AsyncSession, contract_id: int) -> list[ContractNode]:
        """按合同查询全部收费节点（按计划日期升序）。"""
        result = await db.execute(
            select(ContractNode)
            .where(ContractNode.contract_id == contract_id)
            .order_by(ContractNode.plan_date.asc().nullslast(), ContractNode.id)
        )
        return list(result.scalars().all())


# 单例
contract_crud = CRUDContract()
contract_node_crud = CRUDContractNode()
