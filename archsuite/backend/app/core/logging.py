"""日志配置：统一配置 uvicorn / sqlalchemy 日志级别与格式。"""

import logging
import sys


def configure_logging() -> None:
    """配置应用全局日志，控制台输出带时间戳与级别。"""
    fmt = "%(asctime)s | %(levelname)-5.5s | %(name)s | %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(level=logging.INFO, format=fmt, datefmt=datefmt, stream=sys.stdout)

    # 调低第三方库噪音日志
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


# 应用 logger
logger = logging.getLogger("archsuite")
