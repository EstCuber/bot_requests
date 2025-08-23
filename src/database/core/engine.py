
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.core.settings import settings
# TODO: Убрать глобалы!
engine = create_async_engine(settings.DB_URL, echo=True)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
