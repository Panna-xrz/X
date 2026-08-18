"""数据库连接与会话管理：SQLAlchemy 2.0 异步模式。"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# 异步引擎
engine = create_async_engine(
    settings.database_url,
    echo=False,
    future=True,
)

# 异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """所有 ORM 模型的声明式基类（供 alembic 与 create_all 共用）。"""


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI 依赖：注入异步数据库会话，请求结束自动关闭。"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_all() -> None:
    """启动时创建所有表（开发用，生产环境请使用 alembic 迁移）。"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
