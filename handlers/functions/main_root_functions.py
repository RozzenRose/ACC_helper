from custom_classes import user_data, user_selection, user_language
import storage.keyboards as keyboards
from aiogram import types
import storage.messages as messages
from sqlalchemy import text
from DB_settings.DB_engine import engine


def user_initialization(id: int):
    '''Инициализация юзера'''
    user_selection.data_check(user_id=id)  # заносим пользователя в объект для хранения выборов
    user_data.data_check(user_id=id)  # заносим ползователя в объект хранения данных
    user_language.data_check(user_id=id)  # заносим ползователя в объект хранения языка


def lang_select_message():
    '''Создаем объекты для сообщения с выбором языка'''
    # создаем объект клавиатуры
    keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.lang_select, resize_keyboard=True)
    # создаем текст сообщения
    msg_text = messages.lang_select
    return msg_text, keyboard


def start_message(car, track, lang):
    '''Создаем объекты для стартового сообщения'''
    keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.start_message(lang),
                                         resize_keyboard=True,
                                         input_field_placeholder=messages.start_msg_placeholder(lang))
    msg_text = messages.start_message_letter(car, track, lang)
    return msg_text, keyboard


def delete_cache(id):
    '''Отчищаем выборы пользователя и сбрасываем флаги состояния'''
    try:
        user_selection.forget_all(id)  # Забываем выборы пользователя
        user_data.forget_all(id)  # Очищаем кэш пользователя
    except NameError:
        pass


def delete_selection(id):
    '''Отчищаем выборы пользователя'''
    try:
        user_data.forget_all(id)  # Откатываем состояние бота
    except NameError:
        pass


async def trackguide_select(car, track):
    '''Достаем трекгайд из БД'''
    async with engine.connect() as conn:
        answer = await conn.execute(text(f'select track_guide from "Info" as I '
                                         f'inner join "Cars" as C on I.car_id = C.id '
                                         f'inner join "Tracks" as T on I.track_id = T.id '
                                         f"where C.car_name = '{car[1:]}' and T.track_name = '{track[1:]}'"))
        answer = answer.first()
        if answer is not None:
            return answer[0]
        else:
            return None


def reset_select():
    '''Сбрасываем флаги состояний выбора трека и маашины'''
    user_selection.put(id, 'track_selector', False)
    user_selection.put(id, 'car_selector', False)


def car_selection(id, msg):
    '''Устанавливаем автомобиль в качестве выбранного'''
    if msg[0] == '/':
        user_selection.put(id, 'car', msg)
        reset_select()
        return True
    return False


def track_selection(id, msg):
    '''Устанавливаем трассу в качестве выбранной'''
    if msg[0] == '/':
        user_selection.put(id, 'track', msg)
        if user_data.get(id, 'calculator_works'):
            return False
        reset_select()
        return True
    return False
