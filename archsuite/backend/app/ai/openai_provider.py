"""OpenAI 提供商：基于 openai.AsyncOpenAI。"""

from openai import AsyncOpenAI

from app.ai.base import AIMessage, AIProvider
from app.core.config import settings
from app.core.logging import logger


class OpenAIProvider(AIProvider):
    """OpenAI 提供商实现，配置来自 settings。"""

    def __init__(self) -> None:
        self.name = "openai"
        # 客户端复用，连接池化
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
        )
        self.model = settings.openai_model

    async def chat(self, messages: list[AIMessage], **kwargs: object) -> str:
        """多轮对话调用 OpenAI Chat Completions。"""
        # 将统一消息结构转为 OpenAI 入参
        payload = [{"role": m.role, "content": m.content} for m in messages]
        # 仅传递与模型/温度相关的可选参数
        model = str(kwargs.pop("model", self.model))
        temperature = kwargs.pop("temperature", 0.2)
        resp = await self.client.chat.completions.create(
            model=model,
            messages=payload,
            temperature=temperature,
        )
        logger.info("OpenAI chat 调用完成，model=%s", model)
        return resp.choices[0].message.content or ""

    async def complete(self, prompt: str, **kwargs: object) -> str:
        """单次补全：用 user 单条消息走 chat 接口。"""
        return await self.chat([AIMessage(role="user", content=prompt)], **kwargs)
