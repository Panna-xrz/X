"""ORM 模型层：定义所有数据库表结构。"""

from app.models.base import Base, TimestampMixin
from app.models.contact import ContactPerson, ContactType
from app.models.contract import Contract, ContractNode, ContractType
from app.models.project import Project, ProjectExtra
from app.models.project_detail import (
    ProjectBuilding,
    ProjectCultural,
    ProjectMetric,
    ProjectPhysical,
    ProjectSurrounding,
)

__all__ = [
    "Base",
    "TimestampMixin",
    # 项目
    "Project",
    "ProjectExtra",
    "ProjectMetric",
    "ProjectSurrounding",
    "ProjectPhysical",
    "ProjectCultural",
    "ProjectBuilding",
    # 联系单
    "ContactPerson",
    "ContactType",
    # 合同
    "Contract",
    "ContractNode",
    "ContractType",
]
