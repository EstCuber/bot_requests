from sqlalchemy import select, inspect, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.crud.base import CRUDBaseTasks
from src.database.models.models import Service

class CRUDService(CRUDBaseTasks[Service]):
    async def get_services_by_category_id(self, session: AsyncSession, category_id: int, skip: int, limit: int):
        primary_key_of_model = inspect(self.model).primary_key[0]
        stmt = (select(Service).
                where(Service.category_id == category_id).
                order_by(primary_key_of_model).
                offset(skip).
                limit(limit))
        await session.execute(stmt)
        await session.commit()

    async def get_services_count_by_category_id(self, session: AsyncSession, category_id: int):
        primary_key_of_model = inspect(self.model).primary_key[0]

        stmt = (
            select(func.count(primary_key_of_model))
            .where(Service.category_id == category_id)
        )
        result = await session.execute(stmt)
        return result.scalar_one()

    async def pagination_by_category_id(self, session: AsyncSession, category_id: int, skip: int, limit: int) -> list[Service]:

        stmt = (
            select(self.model)
            .filter(self.model.category_id == category_id)
            .order_by(self.model.service_id)
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

service_crud = CRUDService(Service) # объект класса Service для работы с услугами