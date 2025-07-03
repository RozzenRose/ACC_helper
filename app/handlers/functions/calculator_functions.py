from custom_classes import user_data
import storage.keyboards as keyboards
from custom_classes import accurate_calculation
from aiogram import types
import storage.messages as messages
from datetime import timedelta


def fuel_calc_builder(lang):
    '''Создаем объекты для сообщения с выбором калькулятора'''
    keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.calculator_select(lang), resize_keyboard=True,
                                         input_field_placeholder=messages.calculator_msg_placeholder(lang))
    msg = messages.calculator_selector(lang)
    return msg, keyboard


def acc_info_get(id, lang):
    '''Создаем объекты для сообщения с точным калькулятором'''
    fuel_flow = user_data.get(id, 'fuel_flow')
    lap_time = user_data.get(id, 'lap_time')
    race_time = user_data.get(id, 'race_time')
    keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.accure(lang), resize_keyboard=True)
    answer = accurate_calculation(fuel_flow, lap_time, race_time)
    msg = messages.accurate_calculator(fuel_flow, lap_time, race_time, answer, lang)
    return msg, keyboard


def lap_fuel_flow(lang):
    '''Создаем объекты для сообщения с пояснением к указанию расхода топлива на круг'''
    keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.get_info_calc(lang), resize_keyboard=True)
    msg = messages.get_flow(lang)
    return msg, keyboard


def lap_time(lang):
    '''Создаем объекты для сообщения с пояснением к указанию среднего времени круга'''
    keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.get_info_calc(lang), resize_keyboard=True)
    msg = messages.get_lap_time(lang)
    return msg, keyboard


def race_duration(lang):
    '''Создаем объекты для сообщения с пояснением к указанию длительности гонки'''
    keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.get_info_calc(lang), resize_keyboard=True)
    msg = messages.get_race_duration(lang)
    return msg, keyboard


def aprox_builder(lang, aproximate_flow, aproximate_time, race_time, track):
    keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.get_ap_calc(lang), resize_keyboard=True)
    answer = accurate_calculation(aproximate_flow, aproximate_time, race_time)
    msg = messages.aprox_calculation(track, race_time, answer, aproximate_flow, aproximate_time, lang)
    return msg, keyboard


def aprox_calc_builder(lang):
    keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards.get_ap_calc(lang), resize_keyboard=True)
    msg = messages.failed_aprox(lang)
    return msg, keyboard


def flow_read(text):
    F_flow = float(text)
    if F_flow < 0:
        raise ValueError
    return F_flow


def laptime_read(msg):
    split_time = [int(item) for item in msg.split(':')]
    for num in split_time:
        if num < 0:
            raise ValueError
    if len(split_time) == 2:
        lap_time = timedelta(seconds=split_time[0], milliseconds=int(str(split_time[1]).ljust(3, '0')))
    elif len(split_time) == 3:
        lap_time = timedelta(minutes=split_time[0], seconds=split_time[1],
                             milliseconds=int(str(split_time[2]).ljust(3, '0')))
    else:
        raise ValueError
    if lap_time < timedelta(0):
        raise ValueError
    return lap_time


def duration_race(msg):
    split_race_time = [int(item) for item in msg.split(':')]
    for num in split_race_time:
        if num < 0:
            raise ValueError
    if len(split_race_time) == 1:
        race_time = timedelta(minutes=split_race_time[0])
    elif len(split_race_time) == 2:
        race_time = timedelta(hours=split_race_time[0], minutes=split_race_time[1])
    else:
        raise ValueError
    return race_time
