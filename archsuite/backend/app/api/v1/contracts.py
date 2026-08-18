"""商务管理路由：合同 CRUD + AI 生成/审核。"""

from fastapi import APIRouter, Query

from app.api.deps import DbSession
from app.schemas.common import PageResult
from app.schemas.contract import ContractCreate, ContractOut
from app.services import contract_service

router = APIRouter(prefix="/contracts", tags=["商务管理"])


@router.get("/", response_model=PageResult[ContractOut])
async def list_contracts(
    db: DbSession,
    project_id: int | None = Query(None, description="按项目过滤"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> PageResult[ContractOut]:
    """查询合同列表，可按 project_id 过滤。"""
    items = await contract_service.list_(db, project_id=project_id)
    return PageResult[ContractOut](
        items=[ContractOut.model_validate(c) for c in items],
        total=len(items),
        page=page,
        page_size=page_size,
    )


@router.post("/", response_model=ContractOut)
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
    contract_id: int, payload: ContractCreate, db: DbSession
) -> ContractOut:
    """更新合同：以创建 schema 全量更新。"""
    contract = await contract_service.update(db, contract_id, payload)
    return ContractOut.model_validate(contract)


@router.post("/{contract_id}/generate")
async def generate_contract(contract_id: int, db: DbSession) -> dict[str, str]:
    """调用 AI 起草合同正文。"""
    content = await contract_service.generate_contract(db, contract_id)
    return {"contract_id": str(contract_id), "content": content}


@router.post("/{contract_id}/review")
async def review_contract(contract_id: int, db: DbSession) -> dict[str, str]:
    """调用 AI 审核合同条款风险。"""
    result = await contract_service.review_contract(db, contract_id)
    return {"contract_id": str(contract_id), "review": result}
