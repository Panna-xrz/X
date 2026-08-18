"""项目相关模型：Project 主表 + ProjectExtra 扩展信息表（多表存储）。"""

from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Project(Base, TimestampMixin):
    """建筑设计项目主表。"""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # 项目名称
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True, comment="项目名称")
    # 项目编号
    code: Mapped[str] = mapped_column(String(100), nullable=False, index=True, comment="项目编号")
    # 委托方
    client: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="委托方")
    # 项目地点
    location: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="项目地点")
    # 项目类型（住宅/办公/商业/教育等）
    type: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="项目类型")
    # 建设规模（建筑面积等）
    scale: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="建设规模")
    # 开工日期
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True, comment="开工日期")
    # 竣工日期
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True, comment="竣工日期")
    # 项目状态：draft/planning/in-progress/completed/archived
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="draft", server_default="draft", comment="项目状态"
    )
    # 项目描述
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="项目描述")

    # 扩展信息（多表关联）
    extras: Mapped[list["ProjectExtra"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    # 关联合同（一对多）
    contracts: Mapped[list["Contract"]] = relationship(  # noqa: F821
        back_populates="project", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Project {self.code} {self.name}>"


class ProjectExtra(Base, TimestampMixin):
    """项目扩展信息表：以键值对形式存储 AI 提取的扩展字段（用地性质、容积率等）。"""

    __tablename__ = "project_extras"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # 关联项目
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True, comment="项目ID"
    )
    # 字段键，例如 land_use / floor_area_ratio / height_limit / green_ratio
    field_key: Mapped[str] = mapped_column(String(100), nullable=False, comment="扩展字段键")
    # 字段值
    field_value: Mapped[str | None] = mapped_column(Text, nullable=True, comment="扩展字段值")
    # 字段来源 AI 提供商
    ai_source: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="AI来源")

    project: Mapped["Project"] = relationship(back_populates="extras")

    def __repr__(self) -> str:
        return f"<ProjectExtra {self.field_key}={self.field_value}>"
