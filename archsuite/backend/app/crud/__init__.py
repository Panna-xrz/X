"""数据访问层包：导出各模型 CRUD 单例。"""

from app.crud.base import CRUDBase
from app.crud.contact import contact_crud
from app.crud.contract import contract_crud, contract_node_crud
from app.crud.project import project_crud
from app.crud.project_detail import (
    project_building_crud,
    project_cultural_crud,
    project_metric_crud,
    project_physical_crud,
    project_surrounding_crud,
)

__all__ = [
    "CRUDBase",
    "project_crud",
    "project_metric_crud",
    "project_surrounding_crud",
    "project_physical_crud",
    "project_cultural_crud",
    "project_building_crud",
    "contact_crud",
    "contract_crud",
    "contract_node_crud",
]
