from aiogram import types
import message_descriptor

start_message = [[types.KeyboardButton(text=message_descriptor.calc_select)],  # создаем клавиши
                [types.KeyboardButton(text=message_descriptor.car_select), types.KeyboardButton(text=message_descriptor.track_select)],
                [types.KeyboardButton(text=message_descriptor.setups), types.KeyboardButton(text=message_descriptor.track_guide)],
                [types.KeyboardButton(text=message_descriptor.leng_swap), types.KeyboardButton(text=message_descriptor.drop)]]

start_message_en = [[types.KeyboardButton(text=message_descriptor.calc_select_en)],  # создаем клавиши
                   [types.KeyboardButton(text=message_descriptor.car_select_en), types.KeyboardButton(text=message_descriptor.track_select_en)],
                   [types.KeyboardButton(text=message_descriptor.setups_en), types.KeyboardButton(text=message_descriptor.track_guide_en)],
                   [types.KeyboardButton(text=message_descriptor.leng_swap),types.KeyboardButton(text=message_descriptor.drop_en)]]

calculator_select = [[types.KeyboardButton(text=message_descriptor.accur), types.KeyboardButton(text='Примерный')],
                    [types.KeyboardButton(text=message_descriptor.reboot)]]

calculator_select_en = [[types.KeyboardButton(text=message_descriptor.accur_en), types.KeyboardButton(text='Approximate')],
                        [types.KeyboardButton(text=message_descriptor.reboot_en)]]

accure = [[types.KeyboardButton(text=message_descriptor.ff_get)],
        [types.KeyboardButton(text=message_descriptor.lt_get)],
        [types.KeyboardButton(text=message_descriptor.rt_get)],
        [types.KeyboardButton(text=message_descriptor.reboot)]]

accure_en = [[types.KeyboardButton(text=message_descriptor.ff_get_en)],
            [types.KeyboardButton(text=message_descriptor.lt_get_en)],
            [types.KeyboardButton(text=message_descriptor.rt_get_en)],
            [types.KeyboardButton(text=message_descriptor.reboot_en)]]

get_info_calc = [[types.KeyboardButton(text=message_descriptor.back_to_accur)],
              [types.KeyboardButton(text=message_descriptor.reboot)]]

get_info_calc_en = [[types.KeyboardButton(text=message_descriptor.back_to_accur_en)],
              [types.KeyboardButton(text=message_descriptor.reboot_en)]]

get_ap_calc = [[types.KeyboardButton(text=message_descriptor.track_select)],
                [types.KeyboardButton(text=message_descriptor.rt_get)],
                [types.KeyboardButton(text=message_descriptor.reboot)]]

get_ap_calc_en = [[types.KeyboardButton(text=message_descriptor.track_select_en)],
                  [types.KeyboardButton(text=message_descriptor.rt_get_en)],
                  [types.KeyboardButton(text=message_descriptor.reboot_en)]]

only_back = [[types.KeyboardButton(text=message_descriptor.reboot)]]

only_back_en = [[types.KeyboardButton(text=message_descriptor.reboot_en)]]