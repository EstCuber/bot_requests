from typing import Any, Generic, Type, TypeVar
from sqlalchemy import func, select, inspect
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.models import Base

ModelType = TypeVar("ModelType", bound=Base)

class CRUDBaseTasks(Generic[ModelType]):
    """This class is a base class for CRUD operations:
    For working with models: Category, Service."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(self, session: AsyncSession, **kwargs: Any) -> ModelType:

        """Create a new category or service"""
        database_object = self.model(**kwargs)
        session.add(database_object)
        await session.commit()
        await session.refresh(database_object)
        return database_object

    async def get_one(self, session: AsyncSession, **kwargs: Any) -> ModelType | None:
        """Get one category or service"""
        stmt = select(self.model).filter_by(**kwargs)
        result = await session.execute(stmt)
        print(result)
        return result.scalars().first()

    async def exists(self, session: AsyncSession, **kwargs: Any) -> bool:
        """Check if category or service exist"""
        result = await self.get_one(session, **kwargs)
        return result is not None

    async def pagination(self, session: AsyncSession, *, skip: int, limit: int) -> list[ModelType]:
        """Pagination categories or services"""
        primary_key_of_model = inspect(self.model).primary_key[0]

        stmt = (
            select(self.model)
            .order_by(primary_key_of_model)
            .offset(skip)
            .limit(limit)
        )

        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_count(self, session: AsyncSession) -> int:
        """Get count categories or services"""
        primary_key_of_model = inspect(self.model).primary_key[0]

        stmt = (
            select(func.count(primary_key_of_model))
        )
        result = await session.execute(stmt)
        return result.scalar_one()
