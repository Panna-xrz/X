"""AI 提供商工厂：按配置切换并缓存实例，未配置密钥时抛业务异常。"""

from app.ai.anthropic_provider import AnthropicProvider
from app.ai.base import AIProvider
from app.ai.domestic_provider import DomesticProvider
from app.ai.openai_provider import OpenAIProvider
from app.core.config import settings
from app.core.exceptions import AIConfigError
from app.core.logging import logger

# 提供商实例缓存
_provider_cache: dict[str, AIProvider] = {}

# 提供商注册表：名称 → (提供商类, 对应的 API Key 配置项, 环境变量名)
_PROVIDER_REGISTRY: dict[str, tuple[type[AIProvider], str, str]] = {
    "openai": (OpenAIProvider, "openai_api_key", "OPENAI_API_KEY"),
    "anthropic": (AnthropicProvider, "anthropic_api_key", "ANTHROPIC_API_KEY"),
    "domestic": (DomesticProvider, "qwen_api_key", "QWEN_API_KEY"),
}


def get_provider(name: str | None = None) -> AIProvider:
    """根据名称返回 provider 实例，默认读 settings.ai_default_provider。

    实例按名称缓存；对应 API Key 未配置时抛 AIConfigError（503）。
    """
    provider_name = name or settings.ai_default_provider
    # 命中缓存直接返回
    if provider_name in _provider_cache:
        return _provider_cache[provider_name]

    entry = _PROVIDER_REGISTRY.get(provider_name)
    if entry is None:
        # 未知提供商回退到 openai
        logger.warning("未知 AI 提供商 %s，回退到 openai", provider_name)
        provider_name = "openai"
        entry = _PROVIDER_REGISTRY[provider_name]

    provider_cls, key_attr, env_name = entry
    if not getattr(settings, key_attr):
        raise AIConfigError(
            message=f"AI 提供商 {provider_name} 未配置 API Key",
            detail=f"请在 backend/.env 中设置 {env_name}",
        )

    instance = provider_cls()
    _provider_cache[provider_name] = instance
    logger.info("加载 AI 提供商：%s", provider_name)
    return instance
