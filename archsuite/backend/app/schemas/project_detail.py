"""项目详细信息 schema：指标 / 场地周边 / 物理环境 / 人文环境 / 建筑单体，camelCase 契约。"""

from pydantic import Field

from app.schemas.common import CamelSchema, TimestampSchema


# ========== 指标信息 ==========

class ProjectMetricBase(CamelSchema):
    """指标信息基础字段。"""

    land_use: str | None = Field(None, max_length=255, description="场地属性/用地性质")
    site_area: float | None = Field(None, description="场地面积(㎡)")
    far_above: float | None = Field(None, description="地上容积率")
    far_under: float | None = Field(None, description="地下容积率")
    green_ratio: float | None = Field(None, description="绿地率(%)")
    building_density: float | None = Field(None, description="建筑密度(%)")
    height_limit: float | None = Field(None, description="限高(m)")
    total_floor_area: float | None = Field(None, description="总建筑面积(㎡)")
    above_floor_area: float | None = Field(None, description="地上建筑面积(㎡)")
    under_floor_area: float | None = Field(None, description="地下建筑面积(㎡)")
    parking_above: int | None = Field(None, description="地上停车位数")
    parking_under: int | None = Field(None, description="地下停车位数")
    remarks: str | None = Field(None, description="备注")


class ProjectMetricUpsert(ProjectMetricBase):
    """指标信息 upsert 请求（1:1 关系，传则更新，无则创建）。"""

    project_id: int = Field(..., description="项目ID")


class ProjectMetricOut(ProjectMetricBase, TimestampSchema):
    """指标信息响应。"""

    id: int
    project_id: int


# ========== 场地周边 ==========

class ProjectSurroundingBase(CamelSchema):
    """场地周边基础字段。"""

    longitude: float | None = Field(None, description="经度")
    latitude: float | None = Field(None, description="纬度")
    within_200m: str | None = Field(None, description="200m范围周边")
    within_500m: str | None = Field(None, description="500m范围周边")
    within_2000m: str | None = Field(None, description="2000m范围周边")
    nearby_roads: str | None = Field(None, description="临近道路")
    natural_features: str | None = Field(None, description="自然景观")
    transit_info: str | None = Field(None, description="交通便利信息")
    remarks: str | None = Field(None, description="备注")


class ProjectSurroundingUpsert(ProjectSurroundingBase):
    """场地周边 upsert 请求。"""

    project_id: int = Field(..., description="项目ID")


class ProjectSurroundingOut(ProjectSurroundingBase, TimestampSchema):
    """场地周边响应。"""

    id: int
    project_id: int


# ========== 物理环境 ==========

class ProjectPhysicalBase(CamelSchema):
    """物理环境基础字段。"""

    climate_zone: str | None = Field(None, max_length=255, description="气候区")
    prevailing_wind: str | None = Field(None, max_length=255, description="主导风向")
    solar_path: str | None = Field(None, description="日照轨迹")
    annual_precipitation: float | None = Field(None, description="年降水量(mm)")
    groundwater_level: float | None = Field(None, description="地下水位(m)")
    elevation: float | None = Field(None, description="海拔(m)")
    avg_annual_temp: float | None = Field(None, description="年平均气温(℃)")
    extreme_max_temp: float | None = Field(None, description="极端最高温(℃)")
    extreme_min_temp: float | None = Field(None, description="极端最低温(℃)")
    remarks: str | None = Field(None, description="备注")


class ProjectPhysicalUpsert(ProjectPhysicalBase):
    """物理环境 upsert 请求。"""

    project_id: int = Field(..., description="项目ID")


class ProjectPhysicalOut(ProjectPhysicalBase, TimestampSchema):
    """物理环境响应。"""

    id: int
    project_id: int


# ========== 人文环境 ==========

class ProjectCulturalBase(CamelSchema):
    """人文环境基础字段。"""

    cultural_symbols: str | None = Field(None, description="文化符号")
    regional_architecture: str | None = Field(None, description="地域建筑符号")
    urban_color_scheme: str | None = Field(None, description="城市设计色彩属性")
    local_customs: str | None = Field(None, description="地域风俗")
    historical_culture: str | None = Field(None, description="地域历史文化")
    remarks: str | None = Field(None, description="备注")


class ProjectCulturalUpsert(ProjectCulturalBase):
    """人文环境 upsert 请求。"""

    project_id: int = Field(..., description="项目ID")


class ProjectCulturalOut(ProjectCulturalBase, TimestampSchema):
    """人文环境响应。"""

    id: int
    project_id: int


# ========== 建筑单体 ==========

class ProjectBuildingBase(CamelSchema):
    """建筑单体基础字段。"""

    code: str = Field("", max_length=100, description="单体编号")
    name: str = Field(..., max_length=255, description="单体名称")
    building_nature: str | None = Field(None, max_length=255, description="建筑性质")
    building_function: str | None = Field(None, max_length=255, description="建筑功能")
    floors_above: int | None = Field(None, description="地上层数")
    floors_under: int | None = Field(None, description="地下层数")
    height: float | None = Field(None, description="建筑高度(m)")
    floor_area: float | None = Field(None, description="建筑面积(㎡)")
    remarks: str | None = Field(None, description="备注")


class ProjectBuildingCreate(ProjectBuildingBase):
    """建筑单体创建请求。"""

    project_id: int = Field(..., description="项目ID")


class ProjectBuildingUpdate(CamelSchema):
    """建筑单体更新请求：所有字段可选。"""

    code: str | None = Field(None, max_length=100)
    name: str | None = Field(None, max_length=255)
    building_nature: str | None = Field(None, max_length=255)
    building_function: str | None = Field(None, max_length=255)
    floors_above: int | None = None
    floors_under: int | None = None
    height: float | None = None
    floor_area: float | None = None
    remarks: str | None = None


class ProjectBuildingOut(ProjectBuildingBase, TimestampSchema):
    """建筑单体响应。"""

    id: int
    project_id: int
