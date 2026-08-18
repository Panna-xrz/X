"""AI 提供商抽象基类：统一 chat / complete 接口与调用错误包装。"""

from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from dataclasses import dataclass, field

from app.core.exceptions import AICallError, AppException
from app.core.logging import logger


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


@asynccontextmanager
async def wrap_ai_errors(provider_name: str):
    """统一包装 AI 调用异常：业务异常原样抛出，其余转为 AICallError。"""
    try:
        yield
    except AppException:
        raise
    except Exception as exc:
        logger.error("AI 提供商 %s 调用失败：%s", provider_name, exc)
        raise AICallError(
            message=f"AI 服务调用失败（{provider_name}）",
            detail=str(exc),
        ) from exc
