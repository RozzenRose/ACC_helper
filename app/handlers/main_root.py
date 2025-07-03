from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from app import message_descriptor
from aiogram.dispatcher.event.bases import SkipHandler
from app.handlers.functions import main_root_functions as mrf
from app.custom_classes import user_selection, user_language
from app.storage import messages
import os

# Основной рут бота

main_root_router = Router()


@main_root_router.message(Command('start'))  # стартовое сообщение
async def cmd_start(message: Message):
    '''/start - стартовое сообщение'''
    user_id = message.from_user.id
    mrf.user_initialization(user_id)  # инициализация юзера
    language = await user_language.get(user_id)
    if language is None:  # если язык не выбран
        awr_text, keyboard = mrf.lang_select_message()  # собираем сообщение для выбора языка
    else:
        awr_text, keyboard = mrf.start_message(user_selection.get(user_id, 'car'),  # собираем стартовое сообщение
                                               user_selection.get(user_id, 'track'),
                                               language)
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


@main_root_router.message(F.text == message_descriptor.lang_swap)
async def lan_swap(message: Message):
    '''RU 🇷🇺 🔄 EN 🇬🇧 - смена языка'''
    if await user_language.get(message.from_user.id) == 'ENG':
        await user_language.put(message.from_user.id, message.from_user.username, 'RUS')
    else:
        await user_language.put(message.from_user.id, message.from_user.username, 'ENG')
    await cmd_start(message)


@main_root_router.message(F.text.in_({message_descriptor.drop, message_descriptor.drop_en}))
async def caсhe_drop(message: Message):
    '''Сбросить кеш / drop the cache'''
    mrf.delete_cache(message.from_user.id)
    await cmd_start(message)


@main_root_router.message(F.text.in_({message_descriptor.reboot, message_descriptor.reboot_en}))
async def reboot(message: Message):
    '''⬅️ В начало / ️⬅️ To start'''
    mrf.delete_selection(message.from_user.id)
    await cmd_start(message)  # Отправляем ему стартовое сообщение


@main_root_router.message(F.text.in_({message_descriptor.car_select, message_descriptor.car_select_en}))
async def car_selector(message: Message):
    '''🏎️ Выбрать машину / 🏎️ Select a car'''
    user_selection.put(message.from_user.id, 'track_selector', False)
    user_selection.put(message.from_user.id, 'car_selector', True)
    await message.answer(messages.car_select_message(await user_language.get(message.from_user.id)))


@main_root_router.message(F.text.in_({message_descriptor.track_select, message_descriptor.track_select_en}))
async def track_selector(message: Message):
    '''🏁 Выбрать трассу / 🏁 Select a track'''
    user_selection.put(message.from_user.id, 'car_selector', False)
    user_selection.put(message.from_user.id, 'track_selector', True)
    await message.answer(messages.track_select_message(await user_language.get(message.from_user.id)))


@main_root_router.message(F.text.in_({message_descriptor.track_guide, message_descriptor.track_guide_en}))
async def track_guide(message: Message):
    '''📚 Трекгайды / 📚 Trackguides'''
    car = user_selection.get(message.from_user.id, 'car')
    track = user_selection.get(message.from_user.id, 'track')
    if car is None or track is None:
        await cmd_start(message)
        raise SkipHandler
    answer = await mrf.trackguide_select(car, track)
    if answer is None or answer == '':
        await message.answer(messages.fail_tg(await user_language.get(message.from_user.id)))
    else:
        await message.answer(f'{answer}')


@main_root_router.message(F.text.in_({message_descriptor.setups, message_descriptor.setups_en}))
async def setup(message: Message):
    '''🛠 Сетапы / 🛠 Setups'''
    car = user_selection.get(message.from_user.id, 'car')
    track = user_selection.get(message.from_user.id, 'track')
    if car is None or track is None:
        await cmd_start(message)
        raise SkipHandler
    path = f'app/setups/{car[1:]}/{track[1:]}/setups.zip'
    if os.path.isfile(path):
        await message.answer_document(FSInputFile(path))
    else:
        await message.answer(messages.fail_setup(await user_language.get(message.from_user.id)))


@main_root_router.message()
async def handler_selector(message: Message):
    '''Хендлер для перехвата сообщений с выбранными трассами и машинами
       Если в момент перехвата бот не находится в состоянии выбора машины или трассы,
       хендлер вернет сообщение в роутер для проверки в следующих хендлерах'''
    match (message.from_user.id):
        case (id) if user_selection.get(id, 'car_selector'):
            if mrf.car_selection(id, message.text):
                mrf.reset_select(id)
                await cmd_start(message)
                return

        case (id) if user_selection.get(id, 'track_selector'):
            if mrf.track_selection(id, message.text):
                mrf.reset_select(id)
                await cmd_start(message)
                return

    raise SkipHandler
