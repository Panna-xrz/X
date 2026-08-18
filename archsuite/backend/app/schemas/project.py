"""项目相关 schema。"""

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import TimestampSchema


class ProjectBase(BaseModel):
    """项目基础字段（创建/更新共用）。"""

    name: str = Field(..., max_length=255, description="项目名称")
    code: str = Field(..., max_length=100, description="项目编号")
    location: str | None = Field(None, max_length=255, description="项目地点")
    type: str | None = Field(None, max_length=100, description="项目类型")
    scale: str | None = Field(None, max_length=255, description="建设规模")
    description: str | None = Field(None, description="项目描述")


class ProjectCreate(ProjectBase):
    """创建项目请求。"""

    model_config = ConfigDict(from_attributes=True)


class ProjectUpdate(BaseModel):
    """更新项目请求：所有字段可选。"""

    name: str | None = Field(None, max_length=255)
    code: str | None = Field(None, max_length=100)
    location: str | None = Field(None, max_length=255)
    type: str | None = Field(None, max_length=100)
    scale: str | None = Field(None, max_length=255)
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ProjectOut(ProjectBase, TimestampSchema):
    """项目响应：含 id 与时间戳。"""

    id: int


class ProjectExtraOut(BaseModel):
    """项目扩展信息响应。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    field_key: str
    field_value: str | None
    ai_source: str | None
