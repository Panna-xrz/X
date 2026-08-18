"""AI 返回 JSON 解析工具：容忍 markdown 围栏与前后杂文本。"""

import json
import re

_JSON_FENCE_RE = re.compile(r"^```[a-zA-Z]*\s*|\s*```$")


def parse_json_object(text: str) -> dict[str, object] | None:
    """解析文本中的 JSON 对象，失败返回 None。

    兼容以下常见形态：
    - 纯 JSON 文本
    - markdown 代码块包裹（```json ... ```）
    - JSON 前后夹杂说明文字（截取首尾花括号之间的内容）
    """
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = _JSON_FENCE_RE.sub("", cleaned).strip()
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        # 回退：截取首个 { 到最后一个 } 之间的内容再试
        start, end = cleaned.find("{"), cleaned.rfind("}")
        if start == -1 or end <= start:
            return None
        try:
            data = json.loads(cleaned[start : end + 1])
        except json.JSONDecodeError:
            return None
    return data if isinstance(data, dict) else None
