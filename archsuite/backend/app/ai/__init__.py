"""AI 抽象层：多提供商抽象基类 + 工厂 + prompt 模板。"""

from app.ai.base import AIProvider, AIMessage
from app.ai.factory import get_provider

__all__ = ["AIProvider", "AIMessage", "get_provider"]
