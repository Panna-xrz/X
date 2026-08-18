"""JSON 解析工具测试：覆盖 markdown 围栏与杂文本容错。"""

from app.utils.json import parse_json_object


def test_plain_json() -> None:
    """纯 JSON 文本直接解析。"""
    assert parse_json_object('{"a": 1}') == {"a": 1}


def test_json_in_code_fence() -> None:
    """markdown 代码块包裹的 JSON。"""
    text = '```json\n{"a": 1, "b": "x"}\n```'
    assert parse_json_object(text) == {"a": 1, "b": "x"}


def test_json_with_surrounding_text() -> None:
    """JSON 前后夹杂说明文字：截取首尾花括号。"""
    text = '解析结果如下：{"level": "高", "suggestion": "修改付款条款"} 请参考。'
    assert parse_json_object(text) == {"level": "高", "suggestion": "修改付款条款"}


def test_invalid_text_returns_none() -> None:
    """无 JSON 内容返回 None 而非抛异常。"""
    assert parse_json_object("这不是 JSON") is None
    assert parse_json_object("") is None


def test_non_dict_json_returns_none() -> None:
    """数组等非对象 JSON 返回 None。"""
    assert parse_json_object("[1, 2, 3]") is None
