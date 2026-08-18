"""国内 AI 提供商：示例用 httpx 调通义千问 DashScope 兼容接口。

注：通义千问同时提供 OpenAI 兼容接口，可复用 OpenAIProvider 并切换 base_url；
此处为演示原生 httpx 调用 DashScope 的 generation/text-generation 接口。
"""

import httpx

from app.ai.base import AIMessage, AIProvider, wrap_ai_errors
from app.core.config import settings
from app.core.logging import logger

# DashScope 文本生成接口（兼容 OpenAI chat 格式）
_DASHSCOPE_CHAT_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"


class DomesticProvider(AIProvider):
    """国内提供商实现：基于 httpx 调用通义千问。"""

    def __init__(self) -> None:
        self.name = "domestic"
        self.api_key = settings.qwen_api_key
        self.model = settings.qwen_model

    async def chat(self, messages: list[AIMessage], **kwargs: object) -> str:
        """调用 DashScope 兼容接口（OpenAI chat 格式）。"""
        payload = {
            "model": str(kwargs.pop("model", self.model)),
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": float(kwargs.pop("temperature", 0.2)),
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        async with wrap_ai_errors(self.name):
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(_DASHSCOPE_CHAT_URL, json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
        logger.info("通义千问 chat 调用完成，model=%s", payload["model"])
        # 响应结构与 OpenAI 兼容
        return data["choices"][0]["message"]["content"]

    async def complete(self, prompt: str, **kwargs: object) -> str:
        """单次补全：以 user 消息形式调用 chat。"""
        return await self.chat([AIMessage(role="user", content=prompt)], **kwargs)
