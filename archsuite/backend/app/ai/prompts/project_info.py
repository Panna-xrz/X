"""项目信息提取 prompt：让 AI 从项目基本信息提取扩展字段。"""

from app.ai.base import AIMessage

# 系统提示：设定 AI 为建筑项目信息抽取助手
_SYSTEM_PROMPT = (
    "你是一名建筑设计项目信息抽取助手。根据用户提供的项目基本信息，"
    "尽可能从文本中提取以下扩展字段：用地性质（land_use）、容积率（floor_area_ratio）、"
    "建筑限高（height_limit）、绿化率（green_ratio）、建筑密度（building_density）、"
    "用地面积（land_area）、总建筑面积（total_building_area）。"
    "仅输出严格的 JSON，键为字段英文标识，值为字符串或空字符串；不要输出多余说明。"
)


def build_extract_prompt(project_info: str) -> list[AIMessage]:
    """构造项目扩展信息提取的消息列表。

    Args:
        project_info: 项目基本信息文本（名称/地点/规模/描述等）。

    Returns:
        list[AIMessage]: system + user 消息列表。
    """
    user_prompt = (
        "请从以下项目基本信息中抽取扩展字段，"
        "以 JSON 输出（land_use、floor_area_ratio、height_limit、"
        "green_ratio、building_density、land_area、total_building_area）：\n\n"
        f"{project_info}"
    )
    return [
        AIMessage(role="system", content=_SYSTEM_PROMPT),
        AIMessage(role="user", content=user_prompt),
    ]
