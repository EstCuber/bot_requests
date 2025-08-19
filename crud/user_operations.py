from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from crud.models import User

async def add_user(session: AsyncSession,
                   telegram_id: int,
                   username: str
                   ) -> None:
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if user is not None:
        return user

    if user is None:
        user = User(telegram_id=telegram_id, username=username)
        session.add(user)
        await session.commit()

async def add_language(session: AsyncSession,
                       telegram_id: int,
                       lang: str):

    ru_or_eng = update(User).where(User.telegram_id == telegram_id).values(
      language=lang
    )
    await session.execute(ru_or_eng)
    await session.commit()

async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User:
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    user = result.scalars().first()
    return user