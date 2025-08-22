from sqlalchemy import select, update, insert, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.models import User, UserRole, Category, Service


async def get_admins_list(session: AsyncSession) -> list[User]:

    stmt = select(User).where(User.role == UserRole.admin)
    result = await session.execute(stmt)
    admins = result.scalars().all()
    return admins

