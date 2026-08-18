"""通用 schema：camelCase 契约基类与分页结果（泛型）。

契约约定：字段以 Python 习惯的 snake_case 定义，通过 alias_generator
自动生成 camelCase 别名，供前端输入/输出使用；同时开启 populate_by_name
允许字段名直传，from_attributes 支持 ORM 对象直接转换。
"""

from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

T = TypeVar("T")


class CamelSchema(BaseModel):
    """camelCase 契约基类：所有对外 schema 继承此类。

    注意：不开启 serialize_by_alias —— FastAPI 响应序列化本身使用
    by_alias=True（输出 camelCase），而服务层 model_dump() 需要输出
    snake_case 字段名以匹配 ORM 构造器。
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class TimestampSchema(CamelSchema):
    """时间戳混入 schema：输出 createdAt / updatedAt。"""

    created_at: datetime | None = None
    updated_at: datetime | None = None


class PageResult(CamelSchema, Generic[T]):
    """分页结果：对外输出 list / total / page / pageSize。"""

    items: list[T] = Field(serialization_alias="list")
    total: int
    page: int
    page_size: int

    @property
    def pages(self) -> int:
        """总页数。"""
        return (self.total + self.page_size - 1) // self.page_size
