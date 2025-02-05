from DB_settings.DB_config import settings
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False
)