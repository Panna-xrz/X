"""通用 schema：分页参数与分页结果（泛型）。"""

from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PageParams(BaseModel):
    """分页查询参数。"""

    page: int = Field(1, ge=1, description="页码，从1开始")
    page_size: int = Field(20, ge=1, le=100, description="每页条数，1-100")


class PageResult(BaseModel, Generic[T]):
    """分页结果：泛型封装。"""

    items: list[T]
    total: int
    page: int
    page_size: int

    @property
    def pages(self) -> int:
        """总页数。"""
        return (self.total + self.page_size - 1) // self.page_size


class TianAmount(BaseModel):
    """金额信息：用于商务/记账场景。"""

    amount: float = Field(0.0, description="金额")
    currency: str = Field("CNY", description="币种，默认人民币")


class BaseSchema(BaseModel):
    """schema 基类：统一开启 ORM 模式转换与 datetime 序列化。"""

    model_config = {"from_attributes": True}


class TimestampSchema(BaseModel):
    """时间戳混入 schema。"""

    model_config = {"from_attributes": True}
    created_at: datetime | None = None
    updated_at: datetime | None = None
