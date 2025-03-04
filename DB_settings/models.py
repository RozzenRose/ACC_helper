from DB_settings.DB_engine import Base
from sqlalchemy.orm import Mapped, mapped_column

class UsersOrm(Base):
    __tablename__ = 'Users'
    user_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str]
    user_language: Mapped[str]
