"""AI 提供商工厂：按配置切换并缓存实例。"""

from app.ai.base import AIProvider
from app.ai.domestic_provider import DomesticProvider
from app.ai.openai_provider import OpenAIProvider
from app.ai.anthropic_provider import AnthropicProvider
from app.core.config import settings
from app.core.logging import logger

# 提供商实例缓存
_provider_cache: dict[str, AIProvider] = {}

# 提供商注册表
_PROVIDER_REGISTRY: dict[str, type[AIProvider]] = {
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
    "domestic": DomesticProvider,
}


def get_provider(name: str | None = None) -> AIProvider:
    """根据名称返回 provider 实例，默认读 settings.ai_default_provider。

    实例按名称缓存，避免重复创建客户端。
    """
    provider_name = name or settings.ai_default_provider
    # 命中缓存直接返回
    if provider_name in _provider_cache:
        return _provider_cache[provider_name]

    provider_cls = _PROVIDER_REGISTRY.get(provider_name)
    if provider_cls is None:
        # 未知提供商回退到 openai
        logger.warning("未知 AI 提供商 %s，回退到 openai", provider_name)
        provider_name = "openai"
        provider_cls = _PROVIDER_REGISTRY[provider_name]

    instance = provider_cls()
    _provider_cache[provider_name] = instance
    logger.info("加载 AI 提供商：%s", provider_name)
    return instance
