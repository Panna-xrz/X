"""项目相关 schema：camelCase 契约。"""

from datetime import date

from pydantic import Field

from app.schemas.common import CamelSchema, TimestampSchema


class ProjectBase(CamelSchema):
    """项目基础字段（创建/更新共用）。"""

    name: str = Field(..., max_length=255, description="项目名称")
    code: str = Field(..., max_length=100, description="项目编号")
    client: str | None = Field(None, max_length=255, description="委托方")
    location: str | None = Field(None, max_length=255, description="项目地点")
    type: str | None = Field(None, max_length=100, description="项目类型")
    scale: str | None = Field(None, max_length=255, description="建设规模")
    phase: str | None = Field(None, max_length=100, description="项目阶段")
    longitude: float | None = Field(None, description="经度")
    latitude: float | None = Field(None, description="纬度")
    start_date: date | None = Field(None, description="开工日期")
    end_date: date | None = Field(None, description="竣工日期")
    status: str = Field("draft", max_length=50, description="项目状态")
    description: str | None = Field(None, description="项目描述")


class ProjectCreate(ProjectBase):
    """创建项目请求。"""


class ProjectUpdate(CamelSchema):
    """更新项目请求：所有字段可选，仅更新传入字段。"""

    name: str | None = Field(None, max_length=255)
    code: str | None = Field(None, max_length=100)
    client: str | None = Field(None, max_length=255)
    location: str | None = Field(None, max_length=255)
    type: str | None = Field(None, max_length=100)
    scale: str | None = Field(None, max_length=255)
    phase: str | None = Field(None, max_length=100)
    longitude: float | None = None
    latitude: float | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: str | None = Field(None, max_length=50)
    description: str | None = None


class ProjectOut(ProjectBase, TimestampSchema):
    """项目响应：含 id 与时间戳。"""

    id: int


class ProjectExtraOut(TimestampSchema):
    """项目扩展信息响应（键值对行）。"""

    id: int
    project_id: int
    field_key: str
    field_value: str | None
    ai_source: str | None


class ProjectExtraResponse(CamelSchema):
    """项目扩展信息响应：items 为原始键值对列表，fields 为 camelCase 键的对象。"""

    items: list[ProjectExtraOut]
    fields: dict[str, str | None]


class AiExtractResult(CamelSchema):
    """AI 提取扩展信息响应。"""

    project_id: int
    fields: dict[str, str | None]
    raw: str | None = None
