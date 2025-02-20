import DB_settings.models as models
from sqlalchemy.dialects.postgresql.dml import insert
from DB_settings.DB_engine import engine, session_factory
from sqlalchemy.exc import IntegrityError

async def insert_user_data(username):
    async with session_factory() as session:
        user_name = insert(models.UsersOrm).values(username=username)
        user_name = user_name.on_conflict_do_nothing(index_elements=['username'])
        await session.execute(user_name)
        await session.commit()
