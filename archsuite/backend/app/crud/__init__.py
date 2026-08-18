"""数据访问层（CRUD）：每个模块对应一个 CRUD 类，只操作单一模型。"""

from app.crud.base import CRUDBase
from app.crud.contract import CRUDContract
from app.crud.project import CRUDProject

__all__ = ["CRUDBase", "CRUDProject", "CRUDContract"]
