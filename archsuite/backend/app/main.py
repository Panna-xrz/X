"""FastAPI 应用入口：组装中间件、路由、异常处理与静态托管。"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import router as v1_router
from app.core.config import settings
from app.core.database import create_all
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging, logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时初始化日志与数据库表。"""
    configure_logging()
    logger.info("启动 %s", settings.app_name)
    await create_all()
    yield
    logger.info("关闭 %s", settings.app_name)


def create_app() -> FastAPI:
    """创建并配置 FastAPI 应用。"""
    app = FastAPI(
        title=settings.app_name,
        description="建筑设计项目 AI 管理平台 - 后端 API",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS：允许所有来源（开发期）
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 全局异常处理
    register_exception_handlers(app)

    # 注册 v1 路由
    app.include_router(v1_router, prefix="/api/v1")

    @app.get("/health")
    async def health() -> dict[str, str]:
        """健康检查端点。"""
        return {"status": "ok"}

    # 前端静态托管：优先挂载 ../frontend/dist，回退到 static/
    frontend_dir = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    mount_dir = frontend_dir if os.path.isdir(frontend_dir) else static_dir
    # 确保 static 目录存在以避免 StaticFiles 报错
    os.makedirs(mount_dir, exist_ok=True)
    app.mount("/", StaticFiles(directory=mount_dir, html=True), name="frontend")

    return app


app = create_app()
