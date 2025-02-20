from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram import types
import message_descriptor
import storage.messages as messages
import storage.keyboards as keyboards
from custom_classes import user_data, user_selection, user_language
from aiogram.dispatcher.event.bases import SkipHandler
import DB_settings.DB_func as DB_func
from sqlalchemy import text
from DB_settings.DB_engine import engine

# Основной рут бота

main_root_router = Router()


# /start
@main_root_router.message(Command('start'))  # стартовое сообщение
async def cmd_start(message: Message):
    user_selection.__init__(user_id=message.from_user.id)  # заносим ползователя в объект хранения языка
    user_data.__init__(user_id=message.from_user.id)  # заносим ползователя в объект хранения данных
    user_language.__init__(user_id=message.from_user.id)  # заносим ползователя в объект хранения языка
    await DB_func.insert_user_data(message.from_user.username) #запомним имя пользователся
    car = user_selection.get(message.from_user.id, 'car')
    track = user_selection.get(message.from_user.id, 'track')
    if user_language.get(message.from_user.id) is None:
        b_conf = [
            [types.KeyboardButton(text=message_descriptor.eng), types.KeyboardButton(text=message_descriptor.rus)]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=b_conf, resize_keyboard=True)
        await message.answer(f'Select your language:\n'
                             f'Выбери язык:', reply_markup=keyboard, parse_mode='Markdown')
    elif user_language.get(message.from_user.id) == 'RUS':
        # создаем клавиатуру с клавишами
        keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.start_message, resize_keyboard=True,
                                             input_field_placeholder='Чем займемся сегодня?')
        # отправляем пользователю сообщение с клавиатурой
        await message.answer(messages.start_message_letter(car, track),
                             reply_markup=keyboard, parse_mode='Markdown')
    else:
        keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.start_message_en, resize_keyboard=True,
                                             input_field_placeholder='What do you want to do?')
        await message.answer(messages.start_message_letter_en(car, track),
                             reply_markup=keyboard, parse_mode='Markdown')


# Выбор языка: ENG
@main_root_router.message(F.text == message_descriptor.eng)
async def select_eng(message: Message):
    user_language.put(message.from_user.id, 'ENG')
    await cmd_start(message)


# Выбор языка: RUS
@main_root_router.message(F.text == message_descriptor.rus)
async def select_rus(message: Message):
    user_language.put(message.from_user.id, 'RUS')
    await cmd_start(message)


# Выбор языка: смента языка
@main_root_router.message(F.text == message_descriptor.leng_swap)
async def len_swap(message: Message):
    if user_language.get(message.from_user.id) == 'ENG':
        user_language.put(message.from_user.id, 'RUS')
    else:
        user_language.put(message.from_user.id, 'ENG')
    await cmd_start(message)


# Сброс кеша
@main_root_router.message(F.text == message_descriptor.drop)
async def cash_drop(message: Message):
    try:
        user_selection.forget_all(message.from_user.id)  # Забываем его выборы
        user_data.forget_all(message.from_user.id)  # Очищаем кэш пользователя
    except NameError:
        pass
    await cmd_start(message)

@main_root_router.message(F.text == message_descriptor.drop_en)
async def cash_drop_en(message: Message):
    await cash_drop(message)

# кнопка 'В начало'
@main_root_router.message(F.text == message_descriptor.reboot)
async def reboot(message: Message):
    try:
        user_data.forget_all(message.from_user.id)  # Очищаем кэш пользователя
    except NameError:
        pass
    await cmd_start(message)  # Отправляем ему стартовое сообщение


# кнопка 'to start'
@main_root_router.message(F.text == message_descriptor.reboot_en)
async def reboot_en(message: Message):
    await reboot(message)


#/start -> выбор машины
@main_root_router.message(F.text == message_descriptor.car_select)
async def car_selector(message: Message):
    user_selection.put(message.from_user.id, 'track_selector', False)
    user_selection.put(message.from_user.id, 'car_selector', True)
    await message.answer(messages.car_select_message if user_language.get(
        message.from_user.id) == 'RUS' else messages.car_select_message_en)


#/start -> car select
@main_root_router.message(F.text == message_descriptor.car_select_en)
async def car_selector_en(message: Message):
    await car_selector(message)


# /start -> Выбор трассы
@main_root_router.message(F.text == message_descriptor.track_select)
async def track_selector(message: Message):
    user_selection.put(message.from_user.id, 'car_selector', False)
    user_selection.put(message.from_user.id, 'track_selector', True)
    await message.answer(messages.track_select_message if user_language.get(
        message.from_user.id) == 'RUS' else messages.track_select_message_en)


#/start -> track select
@main_root_router.message(F.text == message_descriptor.track_select_en)
async def track_selector_en(message: Message):
    await track_selector(message)


#/start -> трек гайд
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
        try:
            answer = res.first()[0]
            if answer is None or answer == '':
                await message.answer(
                    messages.fail_tg if user_language.get(message.from_user.id) == 'RUS' else messages.fail_tg_en)
            await message.answer(f'{answer}')
        except TypeError:
            await message.answer(
                messages.fail_tg if user_language.get(message.from_user.id) == 'RUS' else messages.fail_tg_en)
    else:
        await cmd_start(message)


#/start -> track guide
@main_root_router.message(F.text == message_descriptor.track_guide_en)
async def track_guide_en(message: Message):
    await track_guide(message)


#/start -> сетпы
@main_root_router.message(F.text == message_descriptor.setups)
async def setup(message: Message):
    car = user_selection.get(message.from_user.id, 'car')
    track = user_selection.get(message.from_user.id, 'track')
    if car != None and track != None:
        try:
            setup_path = FSInputFile(f'setups/{car[1:]}/{track[1:]}/setups.zip')
            await message.answer_document(setup_path)
        except:
            await message.answer('У нас пока нет сетапов для этой машины и трассы' if user_language.get(
                message.from_user.id) == 'RUS' else "We don't have setups for this car on this track yet")
    else:
        await cmd_start(message)


#/start -> setups
@main_root_router.message(F.text == message_descriptor.setups_en)
async def setups_en(message: Message):
    await setup(message)


# хендлер для ответов на выбор трасс или машин
@main_root_router.message()
async def handler_selector(message: Message):
    match (message.from_user.id):
        case (id) if user_selection.get(id, 'car_selector'):
            if message.text[0] == '/':
                user_selection.put(message.from_user.id, 'car', message.text)
                user_selection.put(message.from_user.id, 'track_selector', False)
                user_selection.put(message.from_user.id, 'car_selector', False)
                await cmd_start(message)

        case (id) if user_selection.get(id, 'track_selector'):
            if message.text[0] == '/':
                user_selection.put(message.from_user.id, 'track', message.text)
                if user_data.get(id, 'calculator_works'):
                    raise SkipHandler
                user_selection.put(message.from_user.id, 'track_selector', False)
                user_selection.put(message.from_user.id, 'car_selector', False)
                await cmd_start(message)

    user_selection.put(message.from_user.id, 'track_selector', False)
    user_selection.put(message.from_user.id, 'car_selector', False)
    raise SkipHandler
