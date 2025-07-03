from aiogram import F, Router
from aiogram.types import Message
from aiogram.dispatcher.event.bases import SkipHandler
from app import message_descriptor
from app.custom_classes import user_data, user_language, user_selection
from app.handlers.functions import calculator_functions as cf
import app.DB_settings.DB_func as DB_func
from app.storage import messages

# рут калькулятора

calculator_router = Router()


@calculator_router.message(F.text.in_({message_descriptor.calc_select, message_descriptor.calc_select_en}))
async def fuel_calc(message: Message):
    '''⛽ Калькулятор топлива / ⛽ Fuel calculator'''
    user_data.put(message.from_user.id, 'calculator_works', True)
    msg, keyboard = cf.fuel_calc_builder(await user_language.get(message.from_user.id))
    await message.answer(msg, reply_markup=keyboard)


@calculator_router.message(F.text.in_({message_descriptor.accur,
                                       message_descriptor.accur_en,
                                       message_descriptor.back_to_accur,
                                       message_descriptor.back_to_accur_en}))
async def accure_info_get(message: Message):
    '''Точный / Accurate / Назад / Back'''
    user_data.put(message.from_user.id, 'accure', True)
    msg, keyboard = cf.acc_info_get(message.from_user.id, await user_language.get(message.from_user.id))
    await message.answer(msg, parse_mode='Markdown', reply_markup=keyboard)


@calculator_router.message(F.text.in_({message_descriptor.ff_get, message_descriptor.ff_get_en}))
async def fuel_flow_get(message: Message):
    '''Указать расход топлива на круг / Specify fuel consumption per lap'''
    user_data.put(message.from_user.id, 'calculator', (True, False, False))
    msg, keyboard = cf.lap_fuel_flow(await user_language.get(message.from_user.id))
    await message.answer(msg, reply_markup=keyboard)


@calculator_router.message(F.text.in_({message_descriptor.lt_get, message_descriptor.lt_get_en}))
async def lap_time_get(message: Message):
    '''Указать cреденее время круга / Specify average lap time'''
    user_data.put(message.from_user.id, 'calculator', (False, True, False))
    msg, keyboard = cf.lap_time(await user_language.get(message.from_user.id))
    await message.answer(msg, reply_markup=keyboard, parse_mode='Markdown', resize_keyboard=True)


@calculator_router.message(F.text.in_({message_descriptor.rt_get, message_descriptor.rt_get_en}))  ## запрос длительности гонки
async def race_time_get(message: Message):
    '''Указать длительность гонки / Specify the duration of the race'''
    user_data.put(message.from_user.id, 'calculator', (False, False, True))
    msg, keyboard = cf.race_duration(await user_language.get(message.from_user.id))
    await message.answer(msg, reply_markup=keyboard, parse_mode='Markdown', resize_keyboard=True)


# /start -> калькулятор топлива -> примерный калькулятор топлива
@calculator_router.message(F.text.in_({message_descriptor.aprox, message_descriptor.aprox_en}))
async def aprox_info_get(message: Message):
    '''Примерный / Approximate'''
    user_data.put(message.from_user.id, 'calculator', (False, False, False))
    race_time = user_data.get(message.from_user.id, 'race_time')
    track = user_selection.get(message.from_user.id, 'track')
    lang = await user_language.get(message.from_user.id)
    aproximate_flow, aproximate_time = None, None
    if track is None:
        msg, keyboard = cf.aprox_builder(lang, aproximate_flow, aproximate_time, race_time, track)
    else:
        aproximate_flow, aproximate_time = await DB_func.select_aprox_data(track)
        if aproximate_time is None or aproximate_flow is None:
            msg, keyboard = cf.aprox_calc_builder(lang)
        else:
            msg, keyboard = cf.aprox_builder(lang, aproximate_flow, aproximate_time, race_time, track)

    await message.answer(msg, reply_markup=keyboard, parse_mode='Markdown', resize_keyboard=True)


@calculator_router.message()
async def handler_all_mess(message: Message):
    '''специальный хендлер для обработки текстовых сообщений,
    которые не являются командами или текстом, сгенерированным нажатием кнопок
    этот хендлер должен быть последним в очереди, или содержать исключение raise SkipHandler,
    что бы вернуть объект message обратно dp, для проверки на соответствие следующих хендлеров'''
    lang = await user_language.get(message.from_user.id)
    match (message.from_user.id):
        case (id) if user_data.get(id, 'calculator')[0]:  # сообщение содержит топливо на круг, которое используется в точном калькуляторе
            try:
                F_flow = cf.flow_read(message.text)
                user_data.put(id, 'fuel_flow', F_flow)
                await accure_info_get(message)
            except ValueError:
                await message.answer(messages.abort_flow(lang))

        case (id) if user_data.get(id, 'calculator')[1]:  # сообщение содержит время круга
            try:
                lap_time = cf.laptime_read(message.text)
                user_data.put(id, 'lap_time', lap_time)
                await accure_info_get(message)
            except ValueError:
                await message.answer(messages.abort_lap_time(lang))

        case (id) if user_data.get(id, 'calculator')[2]:  # сообщение содержит длительность гонки
            try:
                race_time = cf.duration_race(message.text)
                user_data.put(id, 'race_time', race_time)
                if user_data.get(id, 'accure'):
                    await accure_info_get(message)
                else:
                    await aprox_info_get(message)
            except ValueError:
                await message.answer(messages.abort_race_duration(lang))

        case (id) if user_selection.get(id, 'track_selector'):  # Выбор трека из примерного калькулятора
            user_selection.put(message.from_user.id, 'track_selector', False)
            if message.text[0] == '/':
                user_selection.put(message.from_user.id, 'track', message.text)
                if user_data.get(id, 'calculator_works'):
                    await aprox_info_get(message)

    raise SkipHandler
