from aiogram import types
import message_descriptor

lang_select = [[types.KeyboardButton(text=message_descriptor.eng), types.KeyboardButton(text=message_descriptor.rus)]]

def start_message(lang):
    if lang == 'RUS':
        return [[types.KeyboardButton(text=message_descriptor.calc_select)],  # создаем клавиши
                [types.KeyboardButton(text=message_descriptor.car_select), types.KeyboardButton(text=message_descriptor.track_select)],
                [types.KeyboardButton(text=message_descriptor.setups), types.KeyboardButton(text=message_descriptor.track_guide)],
                [types.KeyboardButton(text=message_descriptor.leng_swap), types.KeyboardButton(text=message_descriptor.drop)]]
    else:
        return [[types.KeyboardButton(text=message_descriptor.calc_select_en)],  # создаем клавиши
                [types.KeyboardButton(text=message_descriptor.car_select_en), types.KeyboardButton(text=message_descriptor.track_select_en)],
                [types.KeyboardButton(text=message_descriptor.setups_en), types.KeyboardButton(text=message_descriptor.track_guide_en)],
                [types.KeyboardButton(text=message_descriptor.leng_swap),types.KeyboardButton(text=message_descriptor.drop_en)]]

def calculator_select(lang):
    if lang == 'RUS':
        return [[types.KeyboardButton(text=message_descriptor.accur), types.KeyboardButton(text='Примерный')],
                [types.KeyboardButton(text=message_descriptor.reboot)]]
    else:
        return [[types.KeyboardButton(text=message_descriptor.accur_en), types.KeyboardButton(text='Approximate')],
                [types.KeyboardButton(text=message_descriptor.reboot_en)]]

def accure(lang):
    if lang == 'RUS':
        return [[types.KeyboardButton(text=message_descriptor.ff_get)],
                [types.KeyboardButton(text=message_descriptor.lt_get)],
                [types.KeyboardButton(text=message_descriptor.rt_get)],
                [types.KeyboardButton(text=message_descriptor.reboot)]]
    else:
        return [[types.KeyboardButton(text=message_descriptor.ff_get_en)],
                [types.KeyboardButton(text=message_descriptor.lt_get_en)],
                [types.KeyboardButton(text=message_descriptor.rt_get_en)],
                [types.KeyboardButton(text=message_descriptor.reboot_en)]]

def get_info_calc(lang):
    if lang == 'RUS':
        return [[types.KeyboardButton(text=message_descriptor.back_to_accur)],
                [types.KeyboardButton(text=message_descriptor.reboot)]]
    else:
        return [[types.KeyboardButton(text=message_descriptor.back_to_accur_en)],
                [types.KeyboardButton(text=message_descriptor.reboot_en)]]

def get_ap_calc(lang):
    if lang == 'RUS':
        return [[types.KeyboardButton(text=message_descriptor.track_select)],
                [types.KeyboardButton(text=message_descriptor.rt_get)],
                [types.KeyboardButton(text=message_descriptor.reboot)]]
    else:
        return [[types.KeyboardButton(text=message_descriptor.track_select_en)],
                [types.KeyboardButton(text=message_descriptor.rt_get_en)],
                [types.KeyboardButton(text=message_descriptor.reboot_en)]]

def only_back(lang):
    if lang == 'RUS':
        return [[types.KeyboardButton(text=message_descriptor.reboot)]]
    else:
        return [[types.KeyboardButton(text=message_descriptor.reboot_en)]]

