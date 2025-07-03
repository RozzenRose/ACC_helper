import unittest
from unittest.mock import patch, call
from app.handlers.functions import main_root_functions


class TestMainRootFunctions(unittest.IsolatedAsyncioTestCase):
    def test_user_initialization(self):
        '''Тест функции инициализации юзера'''
        with (patch('handlers.functions.main_root_functions.user_selection.data_check') as us_dc,
              patch('handlers.functions.main_root_functions.user_data.data_check') as ud_dc,
              patch('handlers.functions.main_root_functions.user_language.data_check') as ul_dc):
            main_root_functions.user_initialization(12345)
            us_dc.assert_called_once_with(user_id=12345)
            ud_dc.assert_called_once_with(user_id=12345)
            ul_dc.assert_called_once_with(user_id=12345)


    def test_lang_select_message(self):
        '''Тест билдера сообщения с выбором языка'''
        with patch('handlers.functions.main_root_functions.types.ReplyKeyboardMarkup') as kb:
            kb.return_value = 'keyboard_test_return'
            msg_text, keyboard = main_root_functions.lang_select_message()
            kb.assert_called_once()
            self.assertEqual(msg_text, f'Select your language:\nВыбери язык:')
            self.assertEqual(keyboard, 'keyboard_test_return')


    def test_start_message(self):
        '''Тест билдера стартового сообщения'''
        with (patch('handlers.functions.main_root_functions.types.ReplyKeyboardMarkup') as kb,
              patch('handlers.functions.main_root_functions.messages.start_message_letter') as sml):
            kb.return_value = 'keyboard_test_return'
            sml.return_value = 'msg_test_return'
            msg_text, keyboard = main_root_functions.start_message('test_car', 'test_track', 'RUS')
            self.assertEqual(msg_text, 'msg_test_return')
            self.assertEqual(keyboard, 'keyboard_test_return')


    def test_delete_cache(self):
        '''тест хендлера отчистки кеша'''
        with (patch('handlers.functions.main_root_functions.user_selection.forget_all') as us_fa,
              patch('handlers.functions.main_root_functions.user_data.forget_all') as ud_fa):
            main_root_functions.delete_cache(12345)
            us_fa.assert_called_once_with(12345)
            ud_fa.assert_called_once_with(12345)


    def test_delete_selection(self):
        '''тест для хендлера отчистки выборов пользователя'''
        with (patch('handlers.functions.main_root_functions.user_data.forget_all') as ud_fa):
            main_root_functions.delete_selection(12345)
            ud_fa.assert_called_once_with(12345)


    def test_reset_select(self):
        '''тест хендлера сброса флагов'''
        with patch('handlers.functions.main_root_functions.user_selection.put') as us_p:
            main_root_functions.reset_select(12345)
            us_p.assert_has_calls([call(12345, 'track_selector', False),
                                   call(12345, 'car_selector', False)])


    def test_car_selection(self):
        '''тест установки автомобиля в качестве выбранного'''
        with (patch('handlers.functions.main_root_functions.user_selection.put') as us_p,
              patch('handlers.functions.main_root_functions.reset_select') as rs):
            main_root_functions.car_selection(12345, '/test')
            us_p.assert_called_once_with(12345, 'car', '/test')
            rs.assert_called_once_with(12345)


    def test_track_selection(self):
        '''тест устанавливает трассу в качестве выбранной'''
        with (patch('handlers.functions.main_root_functions.user_selection.put') as us_p,
              patch('handlers.functions.main_root_functions.user_data.get') as ud_g,
              patch('handlers.functions.main_root_functions.reset_select') as rs):
            ud_g.return_value = False
            main_root_functions.track_selection(12345, '/track')
            us_p.assert_called_once_with(12345, 'track', '/track')
            ud_g.assert_called_once_with(12345, 'calculator_works')
            rs.assert_called_once_with(12345)
