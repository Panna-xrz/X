"""收费节点业务服务：收费节点 CRUD 与跨合同查询。"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.crud.contract import contract_crud, contract_node_crud
from app.models.contract import ContractNode
from app.schemas.common import PageResult
from app.schemas.contract import ContractNodeCreate, ContractNodeOut, ContractNodeUpdate


async def list_(
    db: AsyncSession,
    contract_id: int | None = None,
    page: int = 1,
    page_size: int = 50,
) -> PageResult[ContractNodeOut]:
    """分页查询收费节点，可按 contract_id 过滤（跨合同查询供记账页面使用）。"""
    filters = [ContractNode.contract_id == contract_id] if contract_id is not None else None
    skip = (page - 1) * page_size
    items = await contract_node_crud.get_multi(
        db, skip=skip, limit=page_size, filters=filters, order_by=ContractNode.id.desc()
    )
    total = await contract_node_crud.count(db, filters)
    return PageResult[ContractNodeOut](
        items=[ContractNodeOut.model_validate(n) for n in items],
        total=total,
        page=page,
        page_size=page_size,
    )


async def list_by_contract(db: AsyncSession, contract_id: int) -> list[ContractNodeOut]:
    """查询某合同的全部收费节点（按计划日期升序）。"""
    await _ensure_contract(db, contract_id)
    nodes = await contract_node_crud.list_by_contract(db, contract_id)
    return [ContractNodeOut.model_validate(n) for n in nodes]


async def create(db: AsyncSession, obj_in: ContractNodeCreate) -> ContractNode:
    """创建收费节点：校验所属合同存在。"""
    await _ensure_contract(db, obj_in.contract_id)
    return await contract_node_crud.create(db, obj_in.model_dump())


async def get(db: AsyncSession, node_id: int) -> ContractNode:
    """获取收费节点，不存在抛 NotFoundError。"""
    node = await contract_node_crud.get(db, node_id)
    if node is None:
        raise NotFoundError(message=f"收费节点 {node_id} 不存在")
    return node


async def update(db: AsyncSession, node_id: int, obj_in: ContractNodeUpdate) -> ContractNode:
    """更新收费节点：仅更新传入字段。"""
    node = await get(db, node_id)
    update_data = obj_in.model_dump(exclude_unset=True)
    return await contract_node_crud.update(db, node, update_data)


async def remove(db: AsyncSession, node_id: int) -> None:
    """删除收费节点。"""
    node = await get(db, node_id)
    await contract_node_crud.remove(db, node)


async def _ensure_contract(db: AsyncSession, contract_id: int) -> None:
    """校验合同存在，不存在抛 NotFoundError。"""
    contract = await contract_crud.get(db, contract_id)
    if contract is None:
        raise NotFoundError(message=f"合同 {contract_id} 不存在")
