"""API 公共依赖：数据库会话与 AI provider 注入。"""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.base import AIProvider
from app.ai.factory import get_provider
from app.core.database import get_db as _get_db


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """重导出数据库会话依赖，供 API 层统一引用。"""
    async for session in _get_db():
        yield session


def get_ai_provider() -> AIProvider:
    """依赖：返回当前配置的 AI provider 实例。"""
    return get_provider()


# 便捷类型别名：依赖注入的数据库会话
DbSession = Annotated[AsyncSession, Depends(get_db)]
# 便捷类型别名：依赖注入的 AI provider
AIProviderDep = Annotated[AIProvider, Depends(get_ai_provider)]
