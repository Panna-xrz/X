"""测试夹具：内存 SQLite 数据库 + 依赖覆盖 + HTTP 客户端。"""

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401  确保所有模型注册到 Base.metadata
from app.core.database import Base, get_db
from app.main import app


@pytest_asyncio.fixture
async def db_engine():
    """内存 SQLite 引擎：StaticPool 保证多连接共享同一内存库。"""
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_engine):
    """直接操作数据库的会话（服务层/CRUD 层测试用）。"""
    maker = async_sessionmaker(
        bind=db_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )
    async with maker() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_engine):
    """HTTP 客户端：覆盖 get_db 依赖指向测试数据库。"""
    maker = async_sessionmaker(
        bind=db_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )

    async def override_get_db():
        async with maker() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
