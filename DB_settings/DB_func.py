import DB_settings.models as models
from sqlalchemy.dialects.postgresql.dml import insert
from DB_settings.DB_engine import session_factory
from sqlalchemy.future import select

async def insert_user_data(user_id: int, username: str, language: str):
    async with session_factory() as session:
        user_data = insert(models.UsersOrm).values(
            user_id=user_id,
            username=username,
            user_language=language
        ).on_conflict_do_update(index_elements=['user_id'],
                                set_={
                                    'username': username,
                                    'user_language': language
                                })
        await session.execute(user_data)
        await session.commit()

async def select_user_leng(user_id: int) -> str:
    async with session_factory() as session:
        lang = select(models.UsersOrm.user_language).where(models.UsersOrm.user_id==user_id)
        result = await session.execute(lang)
        try:
            return result.all()[0][0]
        except (IndexError, AttributeError):
            return None