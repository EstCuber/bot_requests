from sqlalchemy import select, update, insert, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.models import User, UserRole, Category, Service


async def get_admins(session: AsyncSession) -> list[User]:
    stmt = select(User).where(User.role == UserRole.admin)
    result = await session.execute(stmt)
    admins = result.scalars().all()
    return admins

async def orm_create_category(session: AsyncSession, data: dict):
    name = data.get("name")
    description = data.get("description")

    stmt = insert(Category).values(name=name, description=description)
    await session.execute(stmt)
    await session.commit()

async def check_category_exists(session: AsyncSession, category_name: str) -> bool:
    stmt = select(Category).where(Category.name == category_name)
    result = await session.execute(stmt)
    category = result.scalars().first()
    return category is not None

async def orm_pagination_category(session: AsyncSession, offset: int, limit: int) -> list[Category]:
    stmt = select(Category).order_by(Category.category_id).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return result.scalars().all()

async def orm_get_category_count(session: AsyncSession) -> int:
    stmt = select(func.count(Category.category_id))
    result = await session.execute(stmt)
    return result.scalar_one()


async def orm_create_service(session: AsyncSession, data: dict, category_id: int):
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")

    stmt = insert(Service).values(name=name, description=description, price=price, category_id=category_id)
    await session.execute(stmt)
    await session.commit()

async def check_service_exists(session: AsyncSession, service_name: str, category_id: int) -> bool:
    stmt = select(Service).where(and_(Service.name == service_name, Service.category_id == category_id))
    result = await session.execute(stmt)
    service = result.scalars().first()
    return service is not None