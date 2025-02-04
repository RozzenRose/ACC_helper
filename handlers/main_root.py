from aiogram import F, Router
from aiogram.filters import  Command
from aiogram.types import Message, FSInputFile
from aiogram import types
import message_descriptor
from custom_classes import user_data, user_selection
from aiogram.dispatcher.event.bases import SkipHandler

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from DB_config import settings

#Основной рут бота

main_root_router = Router()

engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False
)


#/start
@main_root_router.message(Command('start')) #стартовое сообщение
async def cmd_start(message: Message):
    user_selection.__init__(user_id=message.from_user.id)
    user_data.__init__(user_id=message.from_user.id)      #обьявляем переменную с кэшем
    b_conf = [[types.KeyboardButton(text=message_descriptor.calc_select)],     #создаем клавиши
            [types.KeyboardButton(text=message_descriptor.setups), types.KeyboardButton(text=message_descriptor.track_guide)],
            [types.KeyboardButton(text=message_descriptor.car_select), types.KeyboardButton(text=message_descriptor.track_select)],
            [types.KeyboardButton(text=message_descriptor.drop)]]
    car = user_selection.get(message.from_user.id, 'car')
    track = user_selection.get(message.from_user.id, 'track')
    #создаем клавиатуру с клавишами
    keyboard = types.ReplyKeyboardMarkup(keyboard=b_conf, resize_keyboard=True, input_field_placeholder='Чем займемся сегодня?')
    #отправляем пользователю сообщение с клавиатурой
    await message.answer(f'Привет, это бот-помошник для игры Asetto Corsa Competizione!\n\n'
                         f'Для того чтобы получить сетапы или трекгайды, сначала нужно выбрать трассу и автомобиль.\n\n'
                         f'Для того что бы применить сетапы к машине, открой архив и помести файлы из него в:\n ___C:\\users\\username\\Assetto Corsa Competizione\\Setups\\папка машины\\папка трассы___\n\n'
                         f'🏎️ Текущая машина:   *{car[1:] if car != None else "Нет выбранной машины"}*\n'
                         f'🏁 Текущая трасса:   *{track[1:] if track != None else "Нет выбранной трассы"}*', reply_markup=keyboard, parse_mode='Markdown')

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

@main_root_router.message(F.text == message_descriptor.car_select)
async def fuel_calc(message: Message):
    user_selection.put(message.from_user.id, 'car_selector', True)
    await message.answer(f'Выбери машину:\n\n'
                         f'Porsche:\n'
                         f'/Porsche_922_GT3R\n'
                         f'Ferrari:\n'
                         f'/Ferrari_296_GT3\n'
                         f'Lamborghini:\n'
                         f'/Lamborghini_Huracan_GT3_EVO_2\n\n')

#/start -> Выбор трассы
@main_root_router.message(F.text == message_descriptor.track_select)
async def fuel_calc(message: Message):
    user_selection.put(message.from_user.id, 'track_selector', True)
    await message.answer(f'Выбери трассу:\n'
                         f'/Spa_Francorchamps\n'
                         f'/Monza\n'
                         f'/Misano')

@main_root_router.message(F.text == message_descriptor.track_guide)
async def track_guide(message: Message):
    car = user_selection.get(message.from_user.id, 'car')
    track = user_selection.get(message.from_user.id, 'track')
    if car != None and track != None:
        async with engine.connect() as conn:
            res = await conn.execute(text(f'select track_guide from "Info" '
                                      f'where car_id = (select id from "Cars" '
                                      f"                where car_name = '{car[1:]}') and"
                                      f'      track_id = (select id from "Tracks"'
                                      f"                where track_name = '{track[1:]}')"))
            await message.answer(f'{res.first()[0]}')
    else:
        await cmd_start(message)

@main_root_router.message(F.text == message_descriptor.setups)
async def setup(message: Message):
    car = user_selection.get(message.from_user.id, 'car')
    track = user_selection.get(message.from_user.id, 'track')
    if car != None and track != None:
        try:
            setup_path = FSInputFile(f'setups/{car[1:]}/{track[1:]}/setups.zip')
            await message.answer_document(setup_path)
        except:
            await message.answer('У нас пока нет сетапов для этой машины и трассы')
    else:
        await cmd_start(message)


#хендлер для ответов на выбор трасс или машин
@main_root_router.message()
async def handler_selector(message: Message):
    match (message.from_user.id):
        case (id) if user_selection.get(id, 'car_selector'):
            if message.text[0] == '/':
                user_selection.put(message.from_user.id, 'car', message.text)
                await cmd_start(message)
            user_selection.put(message.from_user.id, 'car_selector', False)

        case (id) if user_selection.get(id, 'track_selector'):
            if message.text[0] == '/':
                user_selection.put(message.from_user.id, 'track', message.text)
                await cmd_start(message)
            user_selection.put(message.from_user.id, 'track_selector', False)

    raise SkipHandler



