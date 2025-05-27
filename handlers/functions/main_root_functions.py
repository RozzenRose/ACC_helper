from custom_classes import user_data, user_selection, user_language
import storage.keyboards as keyboards
from aiogram import types
import storage.messages as messages
from sqlalchemy import text
from DB_settings.DB_engine import engine
from aiogram.dispatcher.event.bases import SkipHandler

def user_initialization(id: int):
    user_selection.data_check(user_id=id)  # заносим ползователя в объект хранения языка
    user_data.data_check(user_id=id)  # заносим ползователя в объект хранения данных
    user_language.data_check(user_id=id)  # заносим ползователя в объект хранения языка

def lang_select_message():
    #создаем объект клавиатуры
    keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.lang_select, resize_keyboard=True)
    #создаем текст сообщения
    msg_text = messages.lang_select
    return [msg_text, keyboard]

def start_message(car, track, lang):
    #создаем клавиатуру
    keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.start_message if lang == 'RUS' else keyboards.start_message_en,
                                         resize_keyboard=True,
                                         input_field_placeholder=messages.start_msg_placeholder if lang == 'RUS' else messages.start_msg_placeholder_en)
    #создаем текст сообщения
    msg_text = (messages.start_message_letter(car, track) if lang == 'RUS' else messages.start_message_letter_en(car, track))
    return [msg_text, keyboard]

def delete_cash(id):
    try:
        user_selection.forget_all(id)  # Забываем выборы пользователя
        user_data.forget_all(id)  # Очищаем кэш пользователя
    except NameError:
        pass

def delete_selection(id):
    try:
        user_data.forget_all(id) # Забываем выборы пользователя
    except NameError:
        pass

async def trackguide_select(car, track):
    async with engine.connect() as conn:
        answer = await conn.execute(text(f'select track_guide from "Info" as I '
                                      f'inner join "Cars" as C on I.car_id = C.id '
                                      f'inner join "Tracks" as T on I.track_id = T.id '
                                      f"where C.car_name = '{car[1:]}' and T.track_name = '{track[1:]}'"))
        try:
            return answer.first()[0]
        except TypeError:
            return None

def reset_select():
    user_selection.put(id, 'track_selector', False)
    user_selection.put(id, 'car_selector', False)

def car_selecion(id, msg):
    if msg[0] == '/':
        user_selection.put(id, 'car', msg)
        reset_select()

def track_selection(id, msg):
    if msg[0] == '/':
        user_selection.put(id, 'track', msg)
        if user_data.get(id, 'calculator_works'):
            raise SkipHandler
        reset_select()
