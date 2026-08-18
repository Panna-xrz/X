"""收费节点路由：跨合同的收费节点查询与管理（供收费记账页面）。"""

from fastapi import APIRouter, Query, status

from app.api.deps import DbSession
from app.schemas.common import PageResult
from app.schemas.contract import ContractNodeCreate, ContractNodeOut, ContractNodeUpdate
from app.services import node_service

router = APIRouter(prefix="/nodes", tags=["收费记账"])


@router.get("", response_model=PageResult[ContractNodeOut])
async def list_nodes(
    db: DbSession,
    contract_id: int | None = Query(None, alias="contractId", description="按合同过滤"),
    page: int = Query(1, ge=1, description="页码，从1开始"),
    page_size: int = Query(50, ge=1, le=500, alias="pageSize", description="每页条数"),
) -> PageResult[ContractNodeOut]:
    """分页查询收费节点，可按 contractId 过滤。"""
    return await node_service.list_(
        db, contract_id=contract_id, page=page, page_size=page_size
    )


@router.post("", response_model=ContractNodeOut, status_code=status.HTTP_201_CREATED)
async def create_node(payload: ContractNodeCreate, db: DbSession) -> ContractNodeOut:
    """创建收费节点。"""
    node = await node_service.create(db, payload)
    return ContractNodeOut.model_validate(node)


@router.put("/{node_id}", response_model=ContractNodeOut)
async def update_node(
    node_id: int, payload: ContractNodeUpdate, db: DbSession
) -> ContractNodeOut:
    """更新收费节点：仅更新传入字段。"""
    node = await node_service.update(db, node_id, payload)
    return ContractNodeOut.model_validate(node)


@router.delete("/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_node(node_id: int, db: DbSession) -> None:
    """删除收费节点。"""
    await node_service.remove(db, node_id)
