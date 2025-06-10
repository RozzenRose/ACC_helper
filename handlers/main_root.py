from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import message_descriptor
from aiogram.dispatcher.event.bases import SkipHandler
from handlers.functions.main_root_functions import *
import os

# Основной рут бота

main_root_router = Router()


@main_root_router.message(Command('start'))  # стартовое сообщение
async def cmd_start(message: Message):
    '''/start - стартовое сообщение'''
    user_id = message.from_user.id
    user_initialization(user_id)  # инициализация юзера
    if await user_language.get(user_id) is None:  # если язык не выбран
        awr_text, keyboard = lang_select_message()  # собиравем сообщение для выбора языка
    else:
        awr_text, keyboard = start_message(user_selection.get(user_id, 'car'),  # собираем стартовое сообщение
                                           user_selection.get(user_id, 'track'),
                                           await user_language.get(user_id))
    await message.answer(awr_text, reply_markup=keyboard, parse_mode='Markdown')  # отправляем сообщение


@main_root_router.message(F.text == message_descriptor.eng)
async def select_eng(message: Message):
    '''ENG - Выбор английского языка'''
    await user_language.put(message.from_user.id, message.from_user.username, 'ENG')
    await cmd_start(message)


@main_root_router.message(F.text == message_descriptor.rus)
async def select_rus(message: Message):
    '''RUS - Выбор русского языка'''
    await user_language.put(message.from_user.id, message.from_user.username, 'RUS')
    await cmd_start(message)


@main_root_router.message(F.text == message_descriptor.leng_swap)
async def len_swap(message: Message):
    '''RU 🇷🇺 🔄 EN 🇬🇧 - смена языка'''
    if await user_language.get(message.from_user.id) == 'ENG':
        await user_language.put(message.from_user.id, message.from_user.username, 'RUS')
    else:
        await user_language.put(message.from_user.id, message.from_user.username, 'ENG')
    await cmd_start(message)


@main_root_router.message(F.text == message_descriptor.drop)
async def caсhe_drop(message: Message):
    '''Сбросить кеш'''
    delete_cache(message.from_user.id)
    await cmd_start(message)


@main_root_router.message(F.text == message_descriptor.drop_en)
async def cache_drop_en(message: Message):
    '''Drop the сache'''
    await caсhe_drop(message)


@main_root_router.message(F.text == message_descriptor.reboot)
async def reboot(message: Message):
    '''⬅️ В начало'''
    delete_selection(message.from_user.id)
    await cmd_start(message)  # Отправляем ему стартовое сообщение


@main_root_router.message(F.text == message_descriptor.reboot_en)
async def reboot_en(message: Message):
    '''⬅️ To start'''
    await reboot(message)


@main_root_router.message(F.text == message_descriptor.car_select)
async def car_selector(message: Message):
    '''🏎️ Выбрать машину'''
    user_selection.put(message.from_user.id, 'track_selector', False)
    user_selection.put(message.from_user.id, 'car_selector', True)
    await message.answer(messages.car_select_message(await user_language.get(message.from_user.id)))


@main_root_router.message(F.text == message_descriptor.car_select_en)
async def car_selector_en(message: Message):
    '''🏎️ Select a car'''
    await car_selector(message)


@main_root_router.message(F.text == message_descriptor.track_select)
async def track_selector(message: Message):
    '''🏁 Выбрать трассу'''
    user_selection.put(message.from_user.id, 'car_selector', False)
    user_selection.put(message.from_user.id, 'track_selector', True)
    await message.answer(messages.track_select_message(await user_language.get(message.from_user.id)))


@main_root_router.message(F.text == message_descriptor.track_select_en)
async def track_selector_en(message: Message):
    '''🏁 Select a track'''
    await track_selector(message)


@main_root_router.message(F.text == message_descriptor.track_guide)
async def track_guide(message: Message):
    '''📚 Трекгайды'''
    car = user_selection.get(message.from_user.id, 'car')
    track = user_selection.get(message.from_user.id, 'track')
    if car is None or track is None:
        await cmd_start(message)
        raise SkipHandler
    answer = await trackguide_select(car, track)
    if answer is None or answer == '':
        await message.answer(messages.fail_tg(await user_language.get(message.from_user.id)))
    else:
        await message.answer(f'{answer}')


@main_root_router.message(F.text == message_descriptor.track_guide_en)
async def track_guide_en(message: Message):
    '''🏁 Select a track'''
    await track_guide(message)


@main_root_router.message(F.text == message_descriptor.setups)
async def setup(message: Message):
    '''🛠 Сетапы'''
    car = user_selection.get(message.from_user.id, 'car')
    track = user_selection.get(message.from_user.id, 'track')
    if car is None or track is None:
        await cmd_start(message)
        raise SkipHandler
    path = f'setups/{car[1:]}/{track[1:]}/setups.zip'
    if os.path.isfile(path):
        await message.answer_document(FSInputFile(path))
    else:
        await message.answer(messages.fail_setup(await user_language.get(message.from_user.id)))


@main_root_router.message(F.text == message_descriptor.setups_en)
async def setups_en(message: Message):
    '''🛠 Setups'''
    await setup(message)


@main_root_router.message()
async def handler_selector(message: Message):
    '''Хендлер для перехвата сообщений с выбранными трассами и машинами
       Если в момент перехвата бот не находится в состоянии выбора машины или трассы,
       хендлер вернет сообщение в роутер для проверки в следующих хендлерах'''
    match (message.from_user.id):
        case (id) if user_selection.get(id, 'car_selector'):
            if car_selection(id, message.text):
                reset_select()
                await cmd_start(message)

        case (id) if user_selection.get(id, 'track_selector'):
            if track_selection(id, message.text):
                reset_select()
                await cmd_start(message)

    raise SkipHandler
