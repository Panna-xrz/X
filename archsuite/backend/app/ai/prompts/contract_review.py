"""合同审核 prompt：让 AI 审核合同条款风险。"""

from app.ai.base import AIMessage

# 系统提示：设定 AI 为合同法律风险审核助手
_SYSTEM_PROMPT = (
    "你是一名建筑设计行业合同审核助手。请审核用户提供的合同正文，"
    "识别其中的法律与商务风险条款（如付款条件、违约责任、知识产权归属、"
    "工期约定、变更索赔条款等），并给出改进建议。"
    "输出结构化 JSON：{\"risks\": [{\"clause\": \"条款\", \"level\": \"高/中/低\", "
    "\"suggestion\": \"建议\"}]}，不要输出多余说明。"
)


def build_review_prompt(contract_text: str) -> list[AIMessage]:
    """构造合同审核的消息列表。

    Args:
        contract_text: 合同正文文本。

    Returns:
        list[AIMessage]: system + user 消息列表。
    """
    user_prompt = f"请审核以下合同条款风险并给出建议：\n\n{contract_text}"
    return [
        AIMessage(role="system", content=_SYSTEM_PROMPT),
        AIMessage(role="user", content=user_prompt),
    ]
