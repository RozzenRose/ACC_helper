from DB_settings.DB_config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False
)

session_factory = async_sessionmaker(engine)