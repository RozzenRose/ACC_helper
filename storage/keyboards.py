from aiogram import types
import message_descriptor

start_message = [[types.KeyboardButton(text=message_descriptor.calc_select)],  # создаем клавиши
                [types.KeyboardButton(text=message_descriptor.setups), types.KeyboardButton(text=message_descriptor.track_guide)],
                [types.KeyboardButton(text=message_descriptor.car_select), types.KeyboardButton(text=message_descriptor.track_select)],
                [types.KeyboardButton(text=message_descriptor.leng_swap), types.KeyboardButton(text=message_descriptor.drop)]]

start_message_en = [[types.KeyboardButton(text=message_descriptor.calc_select_en)],  # создаем клавиши
                   [types.KeyboardButton(text=message_descriptor.setups_en), types.KeyboardButton(text=message_descriptor.track_guide_en)],
                   [types.KeyboardButton(text=message_descriptor.car_select_en), types.KeyboardButton(text=message_descriptor.track_select_en)],
                   [types.KeyboardButton(text=message_descriptor.leng_swap),types.KeyboardButton(text=message_descriptor.drop_en)]]
