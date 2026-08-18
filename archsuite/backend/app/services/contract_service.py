"""合同业务服务：编排 CRUD + AI 起草/审核。"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.factory import get_provider
from app.ai.prompts.contract_review import build_review_prompt
from app.core.exceptions import NotFoundError
from app.core.logging import logger
from app.crud.contract import contract_crud
from app.models.contract import Contract
from app.schemas.contract import ContractCreate


async def list_(db: AsyncSession, project_id: int | None = None) -> list[Contract]:
    """查询合同列表，可按 project_id 过滤。"""
    if project_id is not None:
        return await contract_crud.list_by_project(db, project_id)
    return await contract_crud.get_multi(db, skip=0, limit=100)


async def create(db: AsyncSession, obj_in: ContractCreate) -> Contract:
    """创建合同。"""
    return await contract_crud.create(db, obj_in.model_dump())


async def get(db: AsyncSession, contract_id: int) -> Contract:
    """获取合同详情，不存在抛 NotFoundError。"""
    contract = await contract_crud.get(db, contract_id)
    if contract is None:
        raise NotFoundError(message=f"合同 {contract_id} 不存在")
    return contract


async def update(
    db: AsyncSession, contract_id: int, obj_in: ContractCreate
) -> Contract:
    """更新合同：以创建 schema 全量更新。"""
    contract = await get(db, contract_id)
    update_data = obj_in.model_dump(exclude_unset=True)
    return await contract_crud.update(db, contract, update_data)


async def generate_contract(db: AsyncSession, contract_id: int) -> str:
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
    return content


async def review_contract(db: AsyncSession, contract_id: int) -> str:
    """调用 AI 审核合同条款风险。"""
    contract = await get(db, contract_id)
    if not contract.content_text:
        raise NotFoundError(message="合同尚无正文内容，无法审核")
    messages = build_review_prompt(contract.content_text)
    provider = get_provider()
    result = await provider.chat(messages)
    logger.info("AI 审核合同完成，contract_id=%s", contract_id)
    return result
