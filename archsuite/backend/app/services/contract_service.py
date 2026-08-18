"""合同业务服务：编排 CRUD + AI 起草/审核。"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.factory import get_provider
from app.ai.prompts.contract_review import build_review_prompt
from app.core.exceptions import NotFoundError
from app.core.logging import logger
from app.crud.contract import contract_crud
from app.crud.project import project_crud
from app.models.contract import Contract
from app.schemas.common import PageResult
from app.schemas.contract import (
    ContractCreate,
    ContractGenerateResult,
    ContractOut,
    ContractReviewResult,
    ContractRiskItem,
    ContractUpdate,
)
from app.utils import parse_json_object

# 审核结果字段中文 → 英文键容错映射
_REVIEW_KEY_ALIAS = {
    "条款": "clause",
    "风险等级": "level",
    "等级": "level",
    "建议": "suggestion",
    "改进建议": "suggestion",
}


def _normalize_review_item(item: dict) -> dict:
    """归一化单条风险项：中文键转英文键，缺失键补 None。"""
    normalized: dict[str, str | None] = {}
    for key, value in item.items():
        norm_key = _REVIEW_KEY_ALIAS.get(str(key), str(key))
        if norm_key in ("clause", "level", "suggestion") and value is not None:
            normalized[norm_key] = str(value)
    return normalized


async def list_(
    db: AsyncSession,
    project_id: int | None = None,
    page: int = 1,
    page_size: int = 20,
) -> PageResult[ContractOut]:
    """分页查询合同列表，可按 project_id 过滤（total 为过滤后总数）。"""
    filters = [Contract.project_id == project_id] if project_id is not None else None
    skip = (page - 1) * page_size
    items = await contract_crud.get_multi(
        db, skip=skip, limit=page_size, filters=filters, order_by=Contract.id.desc()
    )
    total = await contract_crud.count(db, filters)
    return PageResult[ContractOut](
        items=[ContractOut.model_validate(c) for c in items],
        total=total,
        page=page,
        page_size=page_size,
    )


async def create(db: AsyncSession, obj_in: ContractCreate) -> Contract:
    """创建合同：校验所属项目存在。"""
    project = await project_crud.get(db, obj_in.project_id)
    if project is None:
        raise NotFoundError(message=f"项目 {obj_in.project_id} 不存在，无法创建合同")
    return await contract_crud.create(db, obj_in.model_dump())


async def get(db: AsyncSession, contract_id: int) -> Contract:
    """获取合同详情，不存在抛 NotFoundError。"""
    contract = await contract_crud.get(db, contract_id)
    if contract is None:
        raise NotFoundError(message=f"合同 {contract_id} 不存在")
    return contract


async def update(db: AsyncSession, contract_id: int, obj_in: ContractUpdate) -> Contract:
    """更新合同：仅更新传入字段。"""
    contract = await get(db, contract_id)
    update_data = obj_in.model_dump(exclude_unset=True)
    return await contract_crud.update(db, contract, update_data)


async def remove(db: AsyncSession, contract_id: int) -> None:
    """删除合同（级联删除收费节点）。"""
    contract = await get(db, contract_id)
    await contract_crud.remove(db, contract)


async def generate_contract(db: AsyncSession, contract_id: int) -> ContractGenerateResult:
    """调用 AI 起草合同正文：基于合同已有信息生成内容并写回 content_text。"""
    contract = await get(db, contract_id)
    # 构造起草提示
    prompt = (
        "你是一名建筑设计行业合同起草助手，请根据以下信息起草一份合同正文：\n"
        f"合同名称：{contract.name}\n"
        f"甲方：{contract.party_a or '待定'}\n"
        f"乙方：{contract.party_b or '待定'}\n"
        f"合同金额：{contract.amount or '待定'}\n"
        "请包含：合同标的、双方权利义务、付款方式、违约责任、争议解决等条款。"
    )
    provider = get_provider()
    content = await provider.complete(prompt)
    logger.info("AI 起草合同完成，contract_id=%s", contract_id)

    # 写回合同正文
    await contract_crud.update(db, contract, {"content_text": content})
    return ContractGenerateResult(contract_id=contract_id, content=content)


async def review_contract(db: AsyncSession, contract_id: int) -> ContractReviewResult:
    """调用 AI 审核合同条款风险，解析为结构化风险清单。"""
    contract = await get(db, contract_id)
    if not contract.content_text:
        raise NotFoundError(message="合同尚无正文内容，请先起草或录入正文后再审核")
    messages = build_review_prompt(contract.content_text)
    provider = get_provider()
    raw = await provider.chat(messages)
    logger.info("AI 审核合同完成，contract_id=%s", contract_id)

    parsed = parse_json_object(raw)
    risks: list[ContractRiskItem] = []
    if parsed is not None and isinstance(parsed.get("risks"), list):
        for item in parsed["risks"]:
            if isinstance(item, dict):
                risks.append(ContractRiskItem(**_normalize_review_item(item)))
    if not risks:
        # 解析失败或空清单：原文回退
        return ContractReviewResult(contract_id=contract_id, risks=[], raw=raw)
    return ContractReviewResult(contract_id=contract_id, risks=risks)
