"""数据访问层包：导出各模型 CRUD 单例。"""

from app.crud.base import CRUDBase
from app.crud.contract import contract_crud, contract_node_crud
from app.crud.project import project_crud

__all__ = [
    "CRUDBase",
    "project_crud",
    "contract_crud",
    "contract_node_crud",
]
