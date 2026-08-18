"""项目详细信息模型：指标 / 场地周边 / 物理环境 / 人文环境 / 建筑单体。

每类信息均以 1:1 或 1:N 关联 Project，多表存储结构清晰，便于 AI 分别提取。
"""

from sqlalchemy import Float, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class ProjectMetric(Base, TimestampMixin):
    """项目指标信息：场地面积、容积率、绿地率、建筑密度等（与 Project 1:1）。"""

    __tablename__ = "project_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True, index=True, comment="项目ID"
    )
    # 场地属性（如：居住用地、商业用地）
    land_use: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="场地属性/用地性质")
    # 场地面积（㎡）
    site_area: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True, comment="场地面积(㎡)")
    # 地上容积率
    far_above: Mapped[float | None] = mapped_column(Numeric(8, 4), nullable=True, comment="地上容积率")
    # 地下容积率
    far_under: Mapped[float | None] = mapped_column(Numeric(8, 4), nullable=True, comment="地下容积率")
    # 绿地率（%）
    green_ratio: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="绿地率(%)")
    # 建筑密度（%）
    building_density: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="建筑密度(%)")
    # 限高（m）
    height_limit: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True, comment="限高(m)")
    # 总建筑面积（㎡）
    total_floor_area: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True, comment="总建筑面积(㎡)")
    # 地上建筑面积（㎡）
    above_floor_area: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True, comment="地上建筑面积(㎡)")
    # 地下建筑面积（㎡）
    under_floor_area: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True, comment="地下建筑面积(㎡)")
    # 停车位数（地上）
    parking_above: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="地上停车位数")
    # 停车位数（地下）
    parking_under: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="地下停车位数")
    # 备注
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    project: Mapped["Project"] = relationship(  # noqa: F821
        back_populates="metric", uselist=False
    )

    def __repr__(self) -> str:
        return f"<ProjectMetric project={self.project_id}>"


class ProjectSurrounding(Base, TimestampMixin):
    """场地周边信息：道路、自然景观、交通等（与 Project 1:1）。"""

    __tablename__ = "project_surroundings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True, index=True, comment="项目ID"
    )
    # 经度（高德坐标系 GCJ-02）
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True, comment="经度")
    # 纬度（高德坐标系 GCJ-02）
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True, comment="纬度")
    # 200m 范围周边描述
    within_200m: Mapped[str | None] = mapped_column(Text, nullable=True, comment="200m范围周边")
    # 500m 范围周边描述
    within_500m: Mapped[str | None] = mapped_column(Text, nullable=True, comment="500m范围周边")
    # 2000m 范围周边描述
    within_2000m: Mapped[str | None] = mapped_column(Text, nullable=True, comment="2000m范围周边")
    # 临近道路（如：城市主干道xx路）
    nearby_roads: Mapped[str | None] = mapped_column(Text, nullable=True, comment="临近道路")
    # 自然景观（河流、公园等）
    natural_features: Mapped[str | None] = mapped_column(Text, nullable=True, comment="自然景观")
    # 交通便利（地铁线路/站点等）
    transit_info: Mapped[str | None] = mapped_column(Text, nullable=True, comment="交通便利信息")
    # 备注
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    project: Mapped["Project"] = relationship(  # noqa: F821
        back_populates="surrounding", uselist=False
    )

    def __repr__(self) -> str:
        return f"<ProjectSurrounding project={self.project_id}>"


class ProjectPhysical(Base, TimestampMixin):
    """物理环境信息：气候区、风向、日照、降水等（与 Project 1:1）。"""

    __tablename__ = "project_physicals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True, index=True, comment="项目ID"
    )
    # 气候区（如：严寒地区A区、寒冷地区、夏热冬冷地区等）
    climate_zone: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="气候区")
    # 主导风向
    prevailing_wind: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="主导风向")
    # 日照轨迹描述
    solar_path: Mapped[str | None] = mapped_column(Text, nullable=True, comment="日照轨迹")
    # 年降水量（mm）
    annual_precipitation: Mapped[float | None] = mapped_column(Numeric(8, 1), nullable=True, comment="年降水量(mm)")
    # 地下水位（m）
    groundwater_level: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True, comment="地下水位(m)")
    # 海拔（m）
    elevation: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True, comment="海拔(m)")
    # 年平均气温（℃）
    avg_annual_temp: Mapped[float | None] = mapped_column(Numeric(5, 1), nullable=True, comment="年平均气温(℃)")
    # 极端最高温（℃）
    extreme_max_temp: Mapped[float | None] = mapped_column(Numeric(5, 1), nullable=True, comment="极端最高温(℃)")
    # 极端最低温（℃）
    extreme_min_temp: Mapped[float | None] = mapped_column(Numeric(5, 1), nullable=True, comment="极端最低温(℃)")
    # 备注
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    project: Mapped["Project"] = relationship(  # noqa: F821
        back_populates="physical", uselist=False
    )

    def __repr__(self) -> str:
        return f"<ProjectPhysical project={self.project_id}>"


class ProjectCultural(Base, TimestampMixin):
    """人文环境信息：文化符号、地域建筑符号、色彩属性、风俗、历史文化（与 Project 1:1）。"""

    __tablename__ = "project_culturals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True, index=True, comment="项目ID"
    )
    # 文化符号
    cultural_symbols: Mapped[str | None] = mapped_column(Text, nullable=True, comment="文化符号")
    # 地域建筑符号
    regional_architecture: Mapped[str | None] = mapped_column(Text, nullable=True, comment="地域建筑符号")
    # 城市设计色彩属性
    urban_color_scheme: Mapped[str | None] = mapped_column(Text, nullable=True, comment="城市设计色彩属性")
    # 地域风俗
    local_customs: Mapped[str | None] = mapped_column(Text, nullable=True, comment="地域风俗")
    # 地域历史文化
    historical_culture: Mapped[str | None] = mapped_column(Text, nullable=True, comment="地域历史文化")
    # 备注
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    project: Mapped["Project"] = relationship(  # noqa: F821
        back_populates="cultural", uselist=False
    )

    def __repr__(self) -> str:
        return f"<ProjectCultural project={self.project_id}>"


class ProjectBuilding(Base, TimestampMixin):
    """建筑单体：为项目地块立项的每个建筑（与 Project 1:N）。"""

    __tablename__ = "project_buildings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True, comment="项目ID"
    )
    # 单体编号
    code: Mapped[str] = mapped_column(String(100), nullable=False, default="", comment="单体编号")
    # 单体名称
    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="单体名称")
    # 建筑性质（如：住宅、商业、办公、教育等）
    building_nature: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="建筑性质")
    # 建筑功能（如：居住、商业运营、办公等）
    building_function: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="建筑功能")
    # 建筑层数（地上）
    floors_above: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="地上层数")
    # 建筑层数（地下）
    floors_under: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="地下层数")
    # 建筑高度（m）
    height: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True, comment="建筑高度(m)")
    # 建筑面积（㎡）
    floor_area: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True, comment="建筑面积(㎡)")
    # 备注
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    project: Mapped["Project"] = relationship(  # noqa: F821
        back_populates="buildings"
    )

    def __repr__(self) -> str:
        return f"<ProjectBuilding {self.name}>"
