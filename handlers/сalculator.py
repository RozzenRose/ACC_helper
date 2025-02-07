from aiogram import F, Router
from aiogram.types import Message
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram import types
import message_descriptor
import storage.messages as messages
import storage.keyboards as keyboards
from custom_classes import user_data, user_language, user_selection, accurate_calculation
from datetime import timedelta
from sqlalchemy import text
from DB_settings.DB_engine import engine

# рут калькулятора

calculator_router = Router()


# /start -> калькулятор топлива
@calculator_router.message(F.text == message_descriptor.calc_select)
async def fuel_calc(message: Message):
    user_data.put(message.from_user.id, 'calculator_works', True)
    if user_language.get(message.from_user.id) == 'RUS':
        keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.calculator_select, resize_keyboard=True,
                                             input_field_placeholder='Выбери тип калькулятора')
    else:
        keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.calculator_select_en, resize_keyboard=True,
                                             input_field_placeholder='Select a type of calculator')
    await message.answer(messages.calculator_selector if user_language.get(
        message.from_user.id) == 'RUS' else messages.calculator_selector_en, reply_markup=keyboard)


@calculator_router.message(F.text == message_descriptor.calc_select_en)
async def fuel_calc_en(message: Message):
    await fuel_calc(message)


# /start -> калькулятор топлива -> точный калькулятор топлива
@calculator_router.message(F.text == message_descriptor.accur)
async def accure_info_get(message: Message):
    user_data.put(message.from_user.id, 'accure', True)
    fuel_flow = user_data.get(message.from_user.id, 'fuel_flow')
    lap_time = user_data.get(message.from_user.id, 'lap_time')
    race_time = user_data.get(message.from_user.id, 'race_time')
    if user_language.get(message.from_user.id) == 'RUS':
        keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.accure, resize_keyboard=True)
        answer = accurate_calculation(fuel_flow, lap_time, race_time)
        await message.answer(messages.accurate_calculator(fuel_flow, lap_time, race_time, answer),
                             parse_mode='Markdown', reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.accure_en, resize_keyboard=True)
        answer = accurate_calculation(fuel_flow, lap_time, race_time)
        await message.answer(messages.accurate_calculator_en(fuel_flow, lap_time, race_time, answer),
                             parse_mode='Markdown', reply_markup=keyboard)


@calculator_router.message(F.text == message_descriptor.accur_en)
async def accure_info_get_en(message: Message):
    await accure_info_get(message)


# ссылка на accure_info_get() через кнопку "Назад"
@calculator_router.message(F.text == message_descriptor.back_to_accur)
async def accure_info_get2(message: Message):
    await accure_info_get(message)


@calculator_router.message(F.text == message_descriptor.back_to_accur_en)
async def accure_info_get2_en(message: Message):
    await accure_info_get(message)


# /start -> калькулятор топлива -> точный калькулятор топлива -> указать расход топлива на круг
@calculator_router.message(F.text == message_descriptor.ff_get)  ## Запрос топлива на круг
async def fuel_flow_get(message: Message):
    fuel_flow = user_data.put(message.from_user.id, 'calculator', (True, False, False))
    if user_language.get(message.from_user.id) == 'RUS':
        keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.get_info_calc, resize_keyboard=True)
    else:
        keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.get_info_calc_en, resize_keyboard=True)
    await message.answer(
        messages.get_flow if user_language.get(message.from_user.id) == 'RUS' else messages.get_flow_en,
        reply_markup=keyboard)


@calculator_router.message(F.text == message_descriptor.ff_get_en)
async def fuel_flow_get_en(message: Message):
    await fuel_flow_get(message)


# /start -> калькулятор топлива -> точный калькулятор торива -> указать среднее время круга
@calculator_router.message(F.text == message_descriptor.lt_get)  ## запрос среднего времени круга
async def lap_time_get(message: Message):
    lap_time = user_data.put(message.from_user.id, 'calculator', (False, True, False))
    if user_language.get(message.from_user.id) == 'RUS':
        keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.get_info_calc, resize_keyboard=True)
    else:
        keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.get_info_calc_en, resize_keyboard=True)
    await message.answer(
        messages.get_lap_time if user_language.get(message.from_user.id) == 'RUS' else messages.get_lap_time_en,
        parse_mode='Markdown', resize_keyboard=True)


@calculator_router.message(F.text == message_descriptor.lt_get_en)
async def lap_time_get_en(message: Message):
    await lap_time_get(message)


# /start -> калькулятор топлива -> точный калькулятор топлива ->  указать длительность гонки
@calculator_router.message(F.text == message_descriptor.rt_get)  ## запрос длительности гонки
async def race_time_get(message: Message):
    race_time = user_data.put(message.from_user.id, 'calculator', (False, False, True))
    if user_language.get(message.from_user.id) == 'RUS':
        keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.get_info_calc, resize_keyboard=True)
    else:
        keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.get_info_calc_en, resize_keyboard=True)
    await message.answer(messages.get_race_duration if user_language.get(
        message.from_user.id) == 'RUS' else messages.get_race_duration_en,
                         parse_mode='Markdown', resize_keyboard=True)


@calculator_router.message(F.text == message_descriptor.rt_get_en)
async def race_time_get_en(message: Message):
    await race_time_get(message)


# /start -> калькулятор топлива -> примерный калькулятор топлива
@calculator_router.message(F.text == message_descriptor.aprox)
async def aprox_info_get(message: Message):
    user_data.put(message.from_user.id, 'calculator', (False, False, False))
    race_time = user_data.get(message.from_user.id, 'race_time')
    track = user_selection.get(message.from_user.id, 'track')
    aproximate_flow, aproximate_time = None, None
    if track is not None:
        async with engine.connect() as conn:
            res = await conn.execute(text(f'select aproximate_flow, aproximate_time '
                                          f'from "Tracks" '
                                          f"where track_name = '{track[1:]}'"))
            res = res.first()
        aproximate_flow = res[0]
        aproximate_time = res[1]
        if aproximate_time is None or aproximate_flow is None:
            if user_language.get(message.from_user.id) == 'RUS':
                keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.only_back, resize_keyboard=True)
                await message.answer(messages.failed_aprox, reply_markup=keyboard)
            else:
                keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.only_back_en, resize_keyboard=True)
                await message.answer(messages.failed_aprox_en, reply_markup=keyboard)
            return
    answer = accurate_calculation(aproximate_flow, aproximate_time, race_time)
    if user_language.get(message.from_user.id) == 'RUS':
        keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.get_ap_calc, resize_keyboard=True)
        await message.answer(messages.aprox_calculation(track, race_time, answer, aproximate_flow, aproximate_time),
                             reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.get_ap_calc_en, resize_keyboard=True)
        await message.answer(messages.aprox_calculation_en(track, race_time, answer, aproximate_flow, aproximate_time),
                             reply_markup=keyboard)

@calculator_router.message(F.text == message_descriptor.aprox_en)
async def aprox_into_get(message: Message):
    await aprox_info_get(message)

# специальный хендлер для обработки текстовых сообщений,
# которые не являются командами или текстом, сгенерированным нажатием кнопок
# этот хендлер должен быть последним в очереди, или содержать исключение raise SkipHandler,
# что бы вернуть объект message обратно dp, для проверки на соответствие следующих хендлеров
@calculator_router.message()
async def handler_all_mess(message: Message):
    match (message.from_user.id):
        case (id) if user_data.get(id, 'calculator')[0]:  # сообщение содержит топливо на круг, которое используется в точном калькуляторе
            try:
                user_data.put(id, 'fuel_flow', float(message.text))
                await accure_info_get(message)
            except ValueError:
                if user_language.get(message.from_user.id) == 'RUS':
                    await message.answer(messages.abort_flow)
                else:
                    await message.answer(messages.abort_flow_en)

        case (id) if user_data.get(id, 'calculator')[1]:  # сообщение содержит время круга
            try:
                split_time = [int(item) for item in message.text.split(':')]
                if len(split_time) == 2:
                    lap_time = timedelta(seconds=split_time[0], milliseconds=int(str(split_time[1]).ljust(3, '0')))
                elif len(split_time) == 3:
                    lap_time = timedelta(minutes=split_time[0], seconds=split_time[1],
                                         milliseconds=int(str(split_time[2]).ljust(3, '0')))
                else:
                    raise ValueError
                user_data.put(id, 'lap_time', lap_time)
                await accure_info_get(message)
            except ValueError:
                if user_language.get(message.from_user.id) == 'RUS':
                    await message.answer(messages.abort_lap_time,
                                         parse_mode='Markdown', resize_keyboard=True)
                else:
                    await message.answer(messages.abort_lap_time_en,
                                         parse_mode='Markdown', resize_keyboard=True)

        case (id) if user_data.get(id, 'calculator')[2]:  # сообщение содержит длительность гонки
            try:
                split_race_time = [int(item) for item in message.text.split(':')]
                if len(split_race_time) == 1:
                    race_time = timedelta(minutes=split_race_time[0])
                elif len(split_race_time) == 2:
                    race_time = timedelta(hours=split_race_time[0], minutes=split_race_time[1])
                else:
                    raise ValueError
                user_data.put(id, 'race_time', race_time)
                if user_data.get(id, 'accure'):
                    await accure_info_get(message)
                else:
                    await aprox_info_get(message)
            except ValueError:
                if user_language.get(message.from_user.id) == 'RUS':
                    await message.answer(messages.abort_race_duration, parse_mode='Markdown', resize_keyboard=True)
                else:
                    await message.answer(messages.abort_race_duration_en, parse_mode='Markdown', resize_keyboard=True)

        case (id) if user_selection.get(id, 'track_selector'):
            user_selection.put(message.from_user.id, 'track_selector', False)
            if message.text[0] == '/':
                user_selection.put(message.from_user.id, 'track', message.text)
                if user_data.get(id, 'calculator_works'):
                    await aprox_info_get(message)

    raise SkipHandler
