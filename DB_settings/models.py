from DB_settings.DB_engine import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import timedelta

class UsersOrm(Base):
    __tablename__ = 'Users'
    user_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str]
    user_language: Mapped[str]

class Tracks(Base):
    __tablename__ = 'Tracks'
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    track_name: Mapped[str]
    turns: Mapped[int]
    aproximate_flow: Mapped[float]
    aproximate_time: Mapped[timedelta]
