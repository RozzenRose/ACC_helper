from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram import types
import message_descriptor
from custom_classes import user_data, FuelCalculator
from datetime import timedelta

# рут калькулятора

calculator_router = Router()

#/start -> калькулятор топлива
@calculator_router.message(F.text == message_descriptor.calc_select)
async def fuel_calc(message: Message):
    user_data.put(message.from_user.id, 'calculator_works', True)
    b_conf = [[types.KeyboardButton(text=message_descriptor.accur), types.KeyboardButton(text='Примерный')],
              [types.KeyboardButton(text=message_descriptor.reboot)]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=b_conf, resize_keyboard=True, input_field_placeholder='Выбери тип калькулятора')
    await message.answer('При примерном расчете, бот посчитает топливо исходя из примерного расхода топлива на круг и премерного времени круга для указанной трассы на автоиобиле класса GT3\n'
                        '\n'
                        'При точном расчете будет необходимо указать ваш средний расход топлива на круг, а так же ваше среднее время круга\n',
                        reply_markup=keyboard)

@calculator_router.message(F.text == message_descriptor.calc_select_en)
async def fuel_calc_en(message: Message):
    await fuel_calc(message)

#/start -> калькулятор топлива -> точный калькулятор топлива
@calculator_router.message(F.text == message_descriptor.accur)
async def accure_info_get(message: Message):
    fuel_flow = user_data.get(message.from_user.id, 'fuel_flow')
    lap_time = user_data.get(message.from_user.id, 'lap_time')
    race_time = user_data.get(message.from_user.id, 'race_time')
    b_conf = [[types.KeyboardButton(text=message_descriptor.ff_get)],
              [types.KeyboardButton(text=message_descriptor.lt_get)],
              [types.KeyboardButton(text=message_descriptor.rt_get)],
              [types.KeyboardButton(text=message_descriptor.reboot)]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=b_conf, resize_keyboard=True)
    answer = FuelCalculator.accurate_calculation(fuel_flow, lap_time, race_time)
    await message.answer(f'Введи неоходимые данные для расчета топлива! \n'
                         f'Любой параметр можно указать заного\n\n'
                         f'Текущие данные:\n\n'
                         f'Расход топлива на круг: \n'
                         f'*{fuel_flow if fuel_flow is not None else "НЕТ ДАННЫХ"}* литров на круг\n\n'
                         f'Среднее вермя круга: \n'
                         f'*{int(lap_time.total_seconds()//60) if lap_time is not None else 'НЕТ ДАННЫХ'}* минут \n'
                         f'*{lap_time.seconds - (int(lap_time.total_seconds()//60) * 60) if lap_time is not None else 'НЕТ ДАННЫХ'}* секунд \n'
                         f'*{str(lap_time.total_seconds()).split('.')[1].ljust(3, '0') if lap_time is not None else 'НЕТ ДАННЫХ'}* миллисекунды \n\n'
                         f'Общее время гонки'
                         f'{int(race_time.total_seconds() // 3600) if race_time is not None else 'НЕТ ДАННЫХ'} часов \n'
                         f'{int(race_time.total_seconds() // 60) - (int(race_time.total_seconds() // 3600) * 60) if race_time is not None else 'НЕТ ДАННЫХ'} минут \n\n'
                         f'На эту гонку нужно залить *{answer}* литров \n'
                         f'Если предусмотрен прогревочный круг, понадобится *{answer + fuel_flow if isinstance(answer, float) else answer}* литров', parse_mode='Markdown', reply_markup=keyboard)

#ссылка на accure_info_get() через кнопку "Назад"
@calculator_router.message(F.text == message_descriptor.back_to_accur)
async def accure_info_get2(message: Message):
    await accure_info_get(message)

#/start -> калькулятор топлива -> точный калькулятор топлива -> указать расход топлива на круг
@calculator_router.message(F.text == message_descriptor.ff_get) ## Запрос топлива на круг
async def fuel_flow_get(message: Message):
    fuel_flow = user_data.put(message.from_user.id, 'calculator', (True, False, False))
    b_conf = [[types.KeyboardButton(text=message_descriptor.back_to_accur)],
              [types.KeyboardButton(text=message_descriptor.reboot)]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=b_conf, resize_keyboard=True)
    await message.answer(f'Введи средний расход топлива на круг, десятые отдели точкой:', reply_markup=keyboard)

#/start -> калькулятор топлива -> точный калькулятор торива -> указать среднее время круга
@calculator_router.message(F.text == message_descriptor.lt_get) ## запрос среднего времени круга
async def lap_time_get(message: Message):
    lap_time = user_data.put(message.from_user.id, 'calculator', (False, True, False))
    b_conf = [[types.KeyboardButton(text=message_descriptor.back_to_accur)],
              [types.KeyboardButton(text=message_descriptor.reboot)]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=b_conf, resize_keyboard=True)
    await message.answer(f'Введи среднее время круга в формате `Min:Sec:Mic` : \n'
        f'Если твой круг меньше минуты, пиши просто `Sec:Mic`', parse_mode='Markdown', resize_keyboard=True)

#/start -> калькулятор топлива -> точный калькулятор топлива ->  указать длительность гонки
@calculator_router.message(F.text == message_descriptor.rt_get) ## запрос длительности гонки
async def race_time_get(message: Message):
    race_time = user_data.put(message.from_user.id, 'calculator', (False, False, True))
    b_conf = [[types.KeyboardButton(text=message_descriptor.back_to_accur)],
              [types.KeyboardButton(text=message_descriptor.reboot)]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=b_conf, resize_keyboard=True)
    await message.answer(f'Бот понимает форматы `Hor:Min` или просто `Min`', parse_mode='Markdown',
                         resize_keyboard=True)

#специальный хендлер для обработки текстовых сообщений,
#которые не являются командами или текстом, сгенерированным нажатием кнопок
#этот хендлер должен быть последним в очереди, или содержать исключение raise SkipHandler,
#что бы вернуть объект message обратно dp, для проверки на соответствие следующих хендлеров
@calculator_router.message()
async def handler_all_mess(message: Message):
    match (message.from_user.id):
        case (id) if user_data.get(id, 'calculator')[0]: #сообщение содержит топливо на круг, которое используется в точном калькуляторе
            try:
                user_data.put(id, 'fuel_flow', float(message.text))
                await accure_info_get(message)
            except ValueError:
                await message.answer(f'То что ты ввел не получилось преобразовать в число, попробуй еще раз\n\n'
                                     f'Введи средний расход топлива на круг, десятые отдели точкой:')

        case (id) if user_data.get(id, 'calculator')[1]: #сообщение содержит время круга
            try:
                split_time = [int(item) for item in message.text.split(':')]
                if len(split_time) == 2:
                    lap_time = timedelta(seconds=split_time[0], milliseconds=int(str(split_time[1]).ljust(3, '0')))
                elif len(split_time) == 3:
                    lap_time = timedelta(minutes=split_time[0], seconds=split_time[1], milliseconds=int(str(split_time[2]).ljust(3, '0')))
                else:
                    raise ValueError
                user_data.put(id, 'lap_time', lap_time)
                await accure_info_get(message)
            except ValueError:
                await message.answer(f'То что ты ввел не получилось преобразовать во время \n \n'
                                     f'Введи среднее время круга в формате `Min:Sec:Mic` : \n'
                                     f'Если твой круг меньше минуты, пиши просто `Sec:Mic`', parse_mode='Markdown',
                                     resize_keyboard=True)

        case (id) if user_data.get(id, 'calculator')[2]: #сообщение содержит длительность гонки
            try:
                split_race_time = [int(item) for item in message.text.split(':')]
                if len(split_race_time) == 1:
                    race_time = timedelta(minutes=split_race_time[0])
                elif len(split_race_time) == 2:
                    race_time = timedelta(hours=split_race_time[0], minutes=split_race_time[1])
                else:
                    raise ValueError
                user_data.put(id, 'race_time', race_time)
                await accure_info_get(message)
            except ValueError:
                await message.answer(f'То что ты ввел не получилось преобрзовать во вреся продолжительности гонки\n\n'
                                     f'Бот понимает форматы `Hor:Min` или просто `Min`')

    raise SkipHandler