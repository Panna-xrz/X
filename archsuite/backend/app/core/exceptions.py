"""全局异常定义与处理器注册。"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    """业务异常基类，携带错误码与消息。"""

    def __init__(self, code: int = 400, message: str = "请求处理失败", detail: str | None = None) -> None:
        self.code = code
        self.message = message
        self.detail = detail
        super().__init__(message)


class NotFoundError(AppException):
    """资源不存在异常。"""

    def __init__(self, message: str = "资源不存在", detail: str | None = None) -> None:
        super().__init__(code=404, message=message, detail=detail)


def register_exception_handlers(app: FastAPI) -> None:
    """注册全局异常处理器到 FastAPI 应用。"""

    @app.exception_handler(AppException)
    async def handle_app_exception(request: Request, exc: AppException) -> JSONResponse:
        """业务异常统一返回 JSON。"""
        return JSONResponse(
            status_code=exc.code,
            content={
                "code": exc.code,
                "message": exc.message,
                "detail": exc.detail,
                "path": request.url.path,
            },
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_exception(request: Request, exc: Exception) -> JSONResponse:
        """未预期异常兜底处理，返回 500。"""
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "message": "服务器内部错误",
                "detail": str(exc),
                "path": request.url.path,
            },
        )
