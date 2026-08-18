"""集中式配置：基于 pydantic-settings 从 .env 读取环境变量。"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """全局配置单例，所有配置项从 .env 文件读取。"""

    # 应用配置
    app_name: str = "ArchSuite Backend"

    # 数据库配置（SQLite + aiosqlite 异步驱动）
    database_url: str = "sqlite+aiosqlite:///./archsuite.db"

    # AI 默认提供商：openai / anthropic / domestic
    ai_default_provider: str = "openai"

    # OpenAI 配置
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"

    # Anthropic 配置
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-5-sonnet-20241022"

    # 通义千问（国内 DashScope 兼容接口）配置
    qwen_api_key: str = ""
    qwen_model: str = "qwen-plus"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


# 配置单例
settings = Settings()
