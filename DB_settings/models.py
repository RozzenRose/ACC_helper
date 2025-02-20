from DB_settings.DB_engine import Base
from sqlalchemy.orm import Mapped, mapped_column

class UsersOrm(Base):
    __tablename__ = 'Users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
