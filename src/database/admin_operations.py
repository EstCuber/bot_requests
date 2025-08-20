from sqlalchemy import select, update, insert
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

async def orm_create_service(session: AsyncSession, name: str, description: str, category_id: int):
    stmt = insert(Service).values(name=name, description=description, category_id=category_id)
    await session.execute(stmt)
    await session.commit()