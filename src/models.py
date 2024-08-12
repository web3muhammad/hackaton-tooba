from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    full_name: Mapped[str]
    thread: Mapped[str]


class Campaign(Base):
    __tablename__ = 'campaign'

    id: Mapped[int] = mapped_column(primary_key=True)
    goal: Mapped[int]
    collected: Mapped[int]
    title: Mapped[str]
    description: Mapped[str]
    link: Mapped[str]
