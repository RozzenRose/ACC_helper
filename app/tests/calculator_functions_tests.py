import unittest
from unittest.mock import patch, call
from app.handlers.functions import calculator_functions
from datetime import timedelta


class TestCalculator(unittest.IsolatedAsyncioTestCase):
    def test_fuel_calc_builder(self):
        with (patch('handlers.functions.calculator_functions.keyboards.calculator_select') as k_cs,
              patch('handlers.functions.calculator_functions.messages.calculator_msg_placeholder') as m_cmp,
              patch('handlers.functions.calculator_functions.types.ReplyKeyboardMarkup') as t_rkm,
              patch('handlers.functions.calculator_functions.messages.calculator_selector') as m_cs):
            t_rkm.return_value = 'test_keyboard'
            m_cs.return_value = 'test_message'
            msg, keyboard = calculator_functions.fuel_calc_builder('RUS')
            k_cs.assert_called_once_with('RUS')
            m_cmp.assert_called_once_with('RUS')
            t_rkm.assert_called_once()
            m_cs.assert_called_once_with('RUS')
            self.assertEqual(msg, 'test_message')
            self.assertEqual(keyboard, 'test_keyboard')

    def test_acc_info_get(self):
        with (patch('handlers.functions.calculator_functions.user_data.get', side_effect=[4.5,
                                                                                   timedelta(minutes=5),
                                                                                   timedelta(minutes=40)]) as ud_g,
              patch('handlers.functions.calculator_functions.keyboards.accure') as k_a,
              patch('handlers.functions.calculator_functions.types.ReplyKeyboardMarkup') as t_rkm,
              patch('handlers.functions.calculator_functions.accurate_calculation') as ac,
              patch('handlers.functions.calculator_functions.messages.accurate_calculator') as m_ac):
            ac.return_value = 90.5
            t_rkm.return_value = 'test_keyboard'
            m_ac.return_value = 'test_message'
            msg, keyboard = calculator_functions.acc_info_get(12345, 'RUS')
            ud_g.assert_has_calls([call(12345, 'fuel_flow'),
                                  call(12345, 'lap_time'),
                                  call(12345, 'race_time')])
            k_a.assert_called_once_with('RUS')
            t_rkm.assert_called_once()
            ac.assert_called_once_with(4.5, timedelta(minutes=5), timedelta(minutes=40))
            m_ac.assert_called_once_with(4.5, timedelta(minutes=5),
                                         timedelta(minutes=40), 90.5, 'RUS')
            self.assertEqual(msg, 'test_message')
            self.assertEqual(keyboard, 'test_keyboard')

    def test_lap_fuel_flow(self):
        with (patch('handlers.functions.calculator_functions.keyboards.get_info_calc') as k_gic,
              patch('handlers.functions.calculator_functions.keyboards.types.ReplyKeyboardMarkup') as t_rkm,
              patch('handlers.functions.calculator_functions.messages.get_flow') as m_gf):
            t_rkm.return_value = 'test_keyboard'
            m_gf.return_value = 'test_message'
            msg, keyboard = calculator_functions.lap_fuel_flow('RUS')
            k_gic.assert_called_once_with('RUS')
            t_rkm.assert_called_once()
            m_gf.assert_called_once_with('RUS')
            self.assertEqual(msg, 'test_message')
            self.assertEqual(keyboard, 'test_keyboard')



