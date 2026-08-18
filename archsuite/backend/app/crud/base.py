"""CRUD 基类：泛型封装单模型的增删改查，全异步。"""

from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

# 模型泛型类型
ModelT = TypeVar("ModelT", bound=Base)


class CRUDBase(Generic[ModelT]):
    """泛型 CRUD 基类，子类指定 model 类型即可复用。"""

    # 子类需指定 ORM 模型类
    model: type[ModelT]

    def __init__(self, model: type[ModelT] | None = None) -> None:
        if model is not None:
            self.model = model

    async def get(self, db: AsyncSession, pk: int) -> ModelT | None:
        """根据主键获取单条记录。"""
        return await db.get(self.model, pk)

    async def get_multi(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        filters: Any = None,
    ) -> list[ModelT]:
        """分页查询多条记录，支持可选过滤条件。"""
        stmt = select(self.model).offset(skip).limit(limit)
        if filters is not None:
            stmt = stmt.where(*filters) if isinstance(filters, list) else stmt.where(filters)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def count(self, db: AsyncSession, filters: Any = None) -> int:
        """统计记录总数。"""
        from sqlalchemy import func

        stmt = select(func.count()).select_from(self.model)
        if filters is not None:
            stmt = stmt.where(*filters) if isinstance(filters, list) else stmt.where(filters)
        result = await db.execute(stmt)
        return int(result.scalar() or 0)

    async def create(self, db: AsyncSession, obj_in: dict[str, Any]) -> ModelT:
        """创建记录。"""
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, db_obj: ModelT, obj_in: dict[str, Any]
    ) -> ModelT:
        """更新记录：以字典形式传入需更新字段。"""
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, db_obj: ModelT) -> None:
        """删除记录。"""
        await db.delete(db_obj)
        await db.commit()
