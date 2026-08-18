"""Anthropic 提供商：基于 anthropic.AsyncAnthropic。"""

from anthropic import AsyncAnthropic

from app.ai.base import AIMessage, AIProvider, wrap_ai_errors
from app.core.config import settings
from app.core.logging import logger


class AnthropicProvider(AIProvider):
    """Anthropic（Claude）提供商实现。"""

    def __init__(self) -> None:
        self.name = "anthropic"
        self.client = AsyncAnthropic(api_key=settings.anthropic_api_key)
        self.model = settings.anthropic_model

    async def chat(self, messages: list[AIMessage], **kwargs: object) -> str:
        """多轮对话调用 Anthropic Messages API。

        Anthropic 要求 system 消息单独传入，此处将 system 消息抽离。
        """
        system_msgs = [m.content for m in messages if m.role == "system"]
        chat_msgs = [m for m in messages if m.role != "system"]
        payload = [{"role": m.role, "content": m.content} for m in chat_msgs]
        model = str(kwargs.pop("model", self.model))
        system_text = "\n".join(system_msgs) if system_msgs else None
        max_tokens = int(kwargs.pop("max_tokens", 2048))
        async with wrap_ai_errors(self.name):
            resp = await self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system_text,
                messages=payload,
            )
        logger.info("Anthropic chat 调用完成，model=%s", model)
        # 提取文本块
        text_parts = [block.text for block in resp.content if hasattr(block, "text")]
        return "".join(text_parts)

    async def complete(self, prompt: str, **kwargs: object) -> str:
        """单次补全：以 user 消息形式调用 chat。"""
        return await self.chat([AIMessage(role="user", content=prompt)], **kwargs)
