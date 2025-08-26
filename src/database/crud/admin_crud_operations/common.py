from sqlalchemy import select, update, insert, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.models import User, UserRole, Category, Service


async def get_admins_list(session: AsyncSession):
    stmt = select(User).where(User.role == UserRole.admin)

    result = await session.execute(stmt)
    admins = result.scalars().all()
    return admins

async def create_admin(session: AsyncSession, telegram_id: int):
    user = update(User).where(User.telegram_id == telegram_id).values(role=UserRole.admin)

    await session.execute(user)
    await session.commit()
    return user