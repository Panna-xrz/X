"""Alembic 迁移环境：从 settings 读取数据库 URL，target_metadata 指向 Base.metadata。"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import settings
from app.core.database import Base
# 导入所有模型，确保 metadata 包含全部表
from app.models import (  # noqa: F401
    BillingRecord,
    Contract,
    ContractNode,
    Project,
    ProjectExtra,
)

# Alembic 配置
config = context.config

# 从 settings 覆盖数据库 URL（同步驱动供 alembic 离线迁移使用）
sync_url = settings.database_url.replace("sqlite+aiosqlite", "sqlite")
config.set_main_option("sqlalchemy.url", sync_url)

# 日志配置
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 迁移目标元数据
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """离线模式：生成 SQL 脚本而不连接数据库。"""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """在线模式：连接数据库执行迁移。"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
