from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram import types
import message_descriptor
import storage.messages as messages
import storage.keyboards as keyboards
from custom_classes import user_data, user_selection, user_language
from aiogram.dispatcher.event.bases import SkipHandler

from sqlalchemy import text
from DB_settings.DB_engine import engine

#Основной рут бота

main_root_router = Router()

#/start
@main_root_router.message(Command('start')) #стартовое сообщение
async def cmd_start(message: Message):
    user_selection.__init__(user_id=message.from_user.id) #заносим ползователя в объект хранения языка
    user_data.__init__(user_id=message.from_user.id)      #заносим ползователя в объект хранения данных
    user_language.__init__(user_id=message.from_user.id)  #заносим ползователя в объект хранения языка
    if user_language.get(message.from_user.id) is None:
        b_conf = [[types.KeyboardButton(text=message_descriptor.eng), types.KeyboardButton(text=message_descriptor.rus)]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=b_conf, resize_keyboard=True)
        await message.answer(f'Select your language:\n'
                                  f'Выбери язык:', reply_markup=keyboard, parse_mode='Markdown')
    elif user_language.get(message.from_user.id) == 'RUS':
        car = user_selection.get(message.from_user.id, 'car')
        track = user_selection.get(message.from_user.id, 'track')
        #создаем клавиатуру с клавишами
        keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.start_message, resize_keyboard=True, input_field_placeholder='Чем займемся сегодня?')
        #отправляем пользователю сообщение с клавиатурой
        await message.answer(f'{messages.start_message_letter}'
                             f'🏎️ Текущая машина:   *{car[1:] if car != None else "Нет выбранной машины"}*\n'
                             f'🏁 Текущая трасса:   *{track[1:] if track != None else "Нет выбранной трассы"}*', reply_markup=keyboard, parse_mode='Markdown')
    else:
        car = user_selection.get(message.from_user.id, 'car')
        track = user_selection.get(message.from_user.id, 'track')
        # создаем клавиатуру с клавишами
        keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.start_message_en, resize_keyboard=True, input_field_placeholder='What do you want to do?')
        # отправляем пользователю сообщение с клавиатурой
        await message.answer(f'{messages.start_message_letter_en}'
                             f'🏎️ Current car:   *{car[1:] if car != None else "No selected car"}*\n'
                             f'🏁 Current track:   *{track[1:] if track != None else "No selected track"}*', reply_markup=keyboard, parse_mode='Markdown')

@main_root_router.message(F.text == message_descriptor.eng)
async def select_eng(message: Message):
    user_language.put(message.from_user.id, 'ENG')
    await cmd_start(message)

@main_root_router.message(F.text == message_descriptor.rus)
async def select_rus(message: Message):
    user_language.put(message.from_user.id, 'RUS')
    await cmd_start(message)

@main_root_router.message(F.text == message_descriptor.leng_swap)
async def len_swap(message: Message):
    if user_language.get(message.from_user.id) == 'ENG':
        user_language.put(message.from_user.id, 'RUS')
    else:
        user_language.put(message.from_user.id, 'ENG')
    await cmd_start(message)

#Сброс кеша
@main_root_router.message(F.text == message_descriptor.drop)
async def cash_drop(message: Message):
    try:
        user_selection.forget_all(message.from_user.id) #Забываем его выборы
        user_data.forget_all(message.from_user.id)      #Очищаем кэш пользователя
    except NameError:
        pass
    await cmd_start(message)

#кнопка 'В начало'
@main_root_router.message(F.text == message_descriptor.reboot)
async def reboot(message: Message):
    try:
        user_data.forget_all(message.from_user.id)  #Очищаем кэш пользователя
    except NameError:
        pass
    await cmd_start(message)                    #Отправляем ему стартовое сообщение

@main_root_router.message(F.text == message_descriptor.reboot_en)
async def reboot_en(message: Message):
    await reboot(message)

@main_root_router.message(F.text == message_descriptor.car_select)
async def car_selector(message: Message):
    user_selection.put(message.from_user.id, 'car_selector', True)
    await message.answer(messages.car_select_message if user_language.get(message.from_user.id) == 'RUS' else messages.car_select_message_en)

@main_root_router.message(F.text == message_descriptor.car_select_en)
async def car_selector_en(message: Message):
    await car_selector(message)

#/start -> Выбор трассы
@main_root_router.message(F.text == message_descriptor.track_select)
async def track_selector(message: Message):
    user_selection.put(message.from_user.id, 'track_selector', True)
    await message.answer(messages.track_select_message if user_language.get(message.from_user.id) == 'RUS' else messages.track_select_message_en)

@main_root_router.message(F.text == message_descriptor.track_select_en)
async def track_selector_en(message: Message):
    await track_selector(message)

@main_root_router.message(F.text == message_descriptor.track_guide)
async def track_guide(message: Message):
    car = user_selection.get(message.from_user.id, 'car')
    track = user_selection.get(message.from_user.id, 'track')
    if car != None and track != None:
        async with engine.connect() as conn:
            res = await conn.execute(text(f'select track_guide from "Info" as I '
                                          f'inner join "Cars" as C on I.car_id = C.id '
                                          f'inner join "Tracks" as T on I.track_id = T.id '
                                          f"where C.car_name = '{car[1:]}' and T.track_name = '{track[1:]}'"))
            await message.answer(f'{res.first()[0]}')
    else:
        await cmd_start(message)

@main_root_router.message(F.text == message_descriptor.track_guide_en)
async def track_guide_en(message: Message):
    await track_guide(message)

@main_root_router.message(F.text == message_descriptor.setups)
async def setup(message: Message):
    car = user_selection.get(message.from_user.id, 'car')
    track = user_selection.get(message.from_user.id, 'track')
    if car != None and track != None:
        try:
            setup_path = FSInputFile(f'setups/{car[1:]}/{track[1:]}/setups.zip')
            await message.answer_document(setup_path)
        except:
            await message.answer('У нас пока нет сетапов для этой машины и трассы' if user_language.get(message.from_user.id) == 'RUS' else "We don't have setups for this car on this track yet")
    else:
        await cmd_start(message)

@main_root_router.message(F.text == message_descriptor.setups_en)
async def setups_en(message: Message):
    await setup(message)

#хендлер для ответов на выбор трасс или машин
@main_root_router.message()
async def handler_selector(message: Message):
    match (message.from_user.id):
        case (id) if user_selection.get(id, 'car_selector'):
            if message.text[0] == '/':
                user_selection.put(message.from_user.id, 'car', message.text)
                user_selection.put(message.from_user.id, 'car_selector', False)
                await cmd_start(message)

        case (id) if user_selection.get(id, 'track_selector'):
            if message.text[0] == '/':
                user_selection.put(message.from_user.id, 'track', message.text)
                if user_data.get(id, 'calculator_works'):
                    raise SkipHandler
                user_selection.put(message.from_user.id, 'track_selector', False)
                await cmd_start(message)

    raise SkipHandler



