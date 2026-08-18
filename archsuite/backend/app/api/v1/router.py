"""v1 路由聚合：挂载各资源子路由。"""

from fastapi import APIRouter

from app.api.v1 import ai, contracts, nodes, projects

router = APIRouter()
# 聚合各资源路由
router.include_router(projects.router)
router.include_router(contracts.router)
router.include_router(nodes.router)
router.include_router(ai.router)
