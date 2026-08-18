"""商务管理路由：合同 CRUD + 收费节点 + AI 起草/审核。"""

from fastapi import APIRouter, Query, status

from app.api.deps import DbSession
from app.schemas.common import PageResult
from app.schemas.contract import (
    ContractCreate,
    ContractGenerateResult,
    ContractNodeOut,
    ContractOut,
    ContractReviewResult,
    ContractUpdate,
)
from app.services import contract_service, node_service

router = APIRouter(prefix="/contracts", tags=["商务管理"])


@router.get("", response_model=PageResult[ContractOut])
async def list_contracts(
    db: DbSession,
    project_id: int | None = Query(None, alias="projectId", description="按项目过滤"),
    page: int = Query(1, ge=1, description="页码，从1开始"),
    page_size: int = Query(20, ge=1, le=100, alias="pageSize", description="每页条数"),
) -> PageResult[ContractOut]:
    """分页查询合同列表，可按 projectId 过滤。"""
    return await contract_service.list_(
        db, project_id=project_id, page=page, page_size=page_size
    )


@router.post("", response_model=ContractOut, status_code=status.HTTP_201_CREATED)
async def create_contract(payload: ContractCreate, db: DbSession) -> ContractOut:
    """创建合同。"""
    contract = await contract_service.create(db, payload)
    return ContractOut.model_validate(contract)


@router.get("/{contract_id}", response_model=ContractOut)
async def get_contract(contract_id: int, db: DbSession) -> ContractOut:
    """获取合同详情。"""
    contract = await contract_service.get(db, contract_id)
    return ContractOut.model_validate(contract)


@router.put("/{contract_id}", response_model=ContractOut)
async def update_contract(
    contract_id: int, payload: ContractUpdate, db: DbSession
) -> ContractOut:
    """更新合同：仅更新传入字段。"""
    contract = await contract_service.update(db, contract_id, payload)
    return ContractOut.model_validate(contract)


@router.delete("/{contract_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contract(contract_id: int, db: DbSession) -> None:
    """删除合同（级联删除收费节点）。"""
    await contract_service.remove(db, contract_id)


@router.get("/{contract_id}/nodes", response_model=list[ContractNodeOut])
async def list_contract_nodes(contract_id: int, db: DbSession) -> list[ContractNodeOut]:
    """查询合同的全部收费节点（按计划日期升序）。"""
    return await node_service.list_by_contract(db, contract_id)


@router.post("/{contract_id}/generate", response_model=ContractGenerateResult)
async def generate_contract(contract_id: int, db: DbSession) -> ContractGenerateResult:
    """调用 AI 起草合同正文并写回。"""
    return await contract_service.generate_contract(db, contract_id)


@router.post("/{contract_id}/review", response_model=ContractReviewResult)
async def review_contract(contract_id: int, db: DbSession) -> ContractReviewResult:
    """调用 AI 审核合同条款风险，返回结构化风险清单。"""
    return await contract_service.review_contract(db, contract_id)
