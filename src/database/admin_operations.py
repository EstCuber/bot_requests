from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from src.database.models.models import User, UserRole


async def get_admins(session: AsyncSession) -> list[User]:
    stmt = select(User).where(User.role == UserRole.admin)
    result = await session.execute(stmt)
    admins = result.scalars().all()
    return admins