"""AI 路由：通用对话调用。"""

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.api.deps import AIProviderDep
from app.ai.base import AIProvider, AIMessage

router = APIRouter(prefix="/ai", tags=["AI"])


class ChatMessage(BaseModel):
    """对话消息。"""

    role: str = Field("user", description="角色：user/assistant/system")
    content: str = Field(..., description="消息内容")


class ChatRequest(BaseModel):
    """通用对话请求。"""

    messages: list[ChatMessage] = Field(..., description="消息列表")
    prompt: str | None = Field(None, description="可选单次补全提示词")


class ChatResponse(BaseModel):
    """通用对话响应。"""

    content: str = Field(..., description="AI 回复内容")
    provider: str = Field(..., description="使用的提供商")


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, provider: AIProviderDep) -> ChatResponse:
    """通用 AI 调用：支持多轮消息或单次补全。"""
    if req.prompt:
        # 单次补全模式
        content = await provider.complete(req.prompt)
    else:
        # 多轮对话模式
        messages = [AIMessage(role=m.role, content=m.content) for m in req.messages]
        content = await provider.chat(messages)
    return ChatResponse(content=content, provider=provider.name)
