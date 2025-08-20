from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import BigInteger, Enum as sqlenum
from enum import Enum

class UserRole(Enum):
    user = "User"
    admin = "Admin"

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "clients"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    language: Mapped[str] = mapped_column(nullable=True)
    role: Mapped[UserRole] = mapped_column(sqlenum(UserRole), nullable=False, default=UserRole.user)

#TODO: создать услугу или товар