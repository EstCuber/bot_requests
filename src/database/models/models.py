from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import BigInteger, Enum as sqlenum, ForeignKey
from enum import Enum

class UserRole(Enum):
    user = "User"
    admin = "Admin"

class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = "telegram_users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    language: Mapped[str] = mapped_column(nullable=True)
    role: Mapped[UserRole] = mapped_column(sqlenum(UserRole), nullable=False, default=UserRole.user)

class Category(Base):

    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    creator_id: Mapped[int] = mapped_column(ForeignKey("telegram_users.telegram_id", ondelete="CASCADE"))
    creator: Mapped[User] = relationship()

    services: Mapped[list["Service"]] = relationship(back_populates="category")

class Service(Base):

    __tablename__ = "services"

    service_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[int] = mapped_column(nullable=True)

    creator_id: Mapped[int] = mapped_column(ForeignKey("telegram_users.telegram_id"))
    creator: Mapped[User] = relationship()

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.category_id", ondelete="CASCADE"))
    category: Mapped[Category] = relationship(back_populates="services")