from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import message_descriptor
from aiogram.dispatcher.event.bases import SkipHandler
from handlers.functions.main_root_functions import*
import os

# Основной рут бота

main_root_router = Router()

# /start
@main_root_router.message(Command('start'))  # стартовое сообщение
async def cmd_start(message: Message):
    user_id = message.from_user.id
    user_initialization(user_id) #инициализация юзера
    if await user_language.get(message.from_user.id) is None: #если язык не выбран
        awr_text, keyboard = lang_select_message() #собиравем сообщение для выбора языка
    else:
        awr_text, keyboard = start_message(user_selection.get(user_id, 'car'), #собираем стартовое сообщение
                                           user_selection.get(user_id, 'track'),
                                           await user_language.get(user_id))
    await message.answer(awr_text, reply_markup=keyboard, parse_mode='Markdown') #отправляем сообщение


# Выбор языка: ENG
@main_root_router.message(F.text == message_descriptor.eng)
async def select_eng(message: Message):
    await user_language.put(message.from_user.id, message.from_user.username, 'ENG')
    await cmd_start(message)


# Выбор языка: RUS
@main_root_router.message(F.text == message_descriptor.rus)
async def select_rus(message: Message):
    await user_language.put(message.from_user.id, message.from_user.username, 'RUS')
    await cmd_start(message)


# Выбор языка: смена языка
@main_root_router.message(F.text == message_descriptor.leng_swap)
async def len_swap(message: Message):
    if await user_language.get(message.from_user.id) == 'ENG':
        await user_language.put(message.from_user.id, message.from_user.username, 'RUS')
    else:
        await user_language.put(message.from_user.id, message.from_user.username, 'ENG')
    await cmd_start(message)


# Сброс кеша
@main_root_router.message(F.text == message_descriptor.drop)
async def cash_drop(message: Message):
    delete_cash(message.from_user.id)
    await cmd_start(message)


@main_root_router.message(F.text == message_descriptor.drop_en)
async def cash_drop_en(message: Message):
    await cash_drop(message)


# кнопка 'В начало'
@main_root_router.message(F.text == message_descriptor.reboot)
async def reboot(message: Message):
    delete_selection(message.from_user.id)
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
    await message.answer(messages.car_select_message
                    if await user_language.get(message.from_user.id) == 'RUS'
                    else messages.car_select_message_en)


#/start -> car select
@main_root_router.message(F.text == message_descriptor.car_select_en)
async def car_selector_en(message: Message):
    await car_selector(message)


# /start -> Выбор трассы
@main_root_router.message(F.text == message_descriptor.track_select)
async def track_selector(message: Message):



    user_selection.put(message.from_user.id, 'car_selector', False)
    user_selection.put(message.from_user.id, 'track_selector', True)
    await message.answer(messages.track_select_message
                   if await user_language.get(message.from_user.id) == 'RUS'
                   else messages.track_select_message_en)


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
        answer = await trackguide_select(car, track)
        if answer is None or answer == '':
            await message.answer(messages.fail_tg
                if await user_language.get(message.from_user.id) == 'RUS'
                else messages.fail_tg_en)
        else:
            await message.answer(f'{answer}')
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
        path = f'setups/{car[1:]}/{track[1:]}/setups.zip'
        if os.path.isfile(path):
            await message.answer_document(FSInputFile(path))
        else:
            await message.answer(messages.fail_setup if await user_language.get(
                message.from_user.id) == 'RUS' else messages.fail_setup_en)
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
            car_selecion(id, message.text)
            await cmd_start(message)

        case (id) if user_selection.get(id, 'track_selector'):
            track_selection(id, message.text)
            await cmd_start(message)

    reset_select()
    raise SkipHandler
