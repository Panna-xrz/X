"""AI 提供商抽象基类：统一 chat / complete 接口。"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class AIMessage:
    """统一消息结构：role（user/assistant/system）+ content。"""

    role: str
    content: str


@dataclass
class AIProvider(ABC):
    """AI 提供商抽象基类，子类实现 chat / complete。

    所有 provider 必须实现 chat 与 complete 两个异步方法。
    """

    # 提供商名称
    name: str = field(default="base")

    @abstractmethod
    async def chat(self, messages: list[AIMessage], **kwargs: object) -> str:
        """多轮对话：接收消息列表，返回 AI 回复文本。"""
        ...

    @abstractmethod
    async def complete(self, prompt: str, **kwargs: object) -> str:
        """单次补全：接收提示词，返回补全文本。"""
        ...
