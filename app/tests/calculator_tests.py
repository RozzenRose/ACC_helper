import unittest
from unittest.mock import patch, AsyncMock, call
from aiogram.types import Message, User
from handlers import calculator
from aiogram.dispatcher.event.bases import SkipHandler
from datetime import timedelta


class TestCalculator(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        '''Инициализация мок-объекта сообщения'''
        self.mock_message = AsyncMock(spec=Message)
        self.mock_message.from_user = User(id=12345, username='test_user', is_bot=False, first_name="Test")
        self.mock_message.answer = AsyncMock()
        self.mock_message.answer_document = AsyncMock()
        self.mock_message.text = 'test_text'


    async def test_fuel_calc(self):
        '''тест стартового сообщения калькулятора'''
        with (patch('handlers.calculator.user_data.put') as ud_p,
              patch('handlers.calculator.cf.fuel_calc_builder') as fcb,
              patch('handlers.calculator.user_language.get', new_callable=AsyncMock) as ul_g):
            fcb.return_value = 'test_msg', 'test_keyboard'
            await calculator.fuel_calc(self.mock_message)
            ud_p.assert_called_once_with(12345, 'calculator_works', True)
            ul_g.assert_called_once_with(12345)
            fcb.assert_called_once()
            self.mock_message.answer.assert_called_once()


    async def test_accure_info_get(self):
        '''тест сообщения точного калькулятора'''
        with (patch('handlers.calculator.user_data.put') as ud_p,
              patch('handlers.calculator.cf.acc_info_get') as aig,
              patch('handlers.calculator.user_language.get', new_callable=AsyncMock) as ul_g):
            aig.return_value = 'test_msg', 'test_keyboard'
            await calculator.accure_info_get(self.mock_message)
            ud_p.assert_called_once_with(12345, 'accure', True)
            ul_g.assert_called_once_with(12345)
            aig.assert_called_once()
            self.mock_message.answer.assert_called_once()


    async def test_fuel_flow_get(self):
        '''тест сообщения, которое просит указать расход топлива на круг'''
        with (patch('handlers.calculator.user_data.put') as ud_p,
              patch('handlers.calculator.cf.lap_fuel_flow') as lff,
              patch('handlers.calculator.user_language.get', new_callable=AsyncMock) as ul_g):
            lff.return_value = 'test_msg', 'test_keyboard'
            await calculator.fuel_flow_get(self.mock_message)
            ud_p.assert_called_once_with(12345, 'calculator', (True, False, False))
            ul_g.assert_called_once_with(12345)
            lff.assert_called_once()
            self.mock_message.answer.assert_called_once()


    async def test_lap_time_get(self):
        '''тест сообщения, которое просит указать среднее время круга'''
        with (patch('handlers.calculator.user_data.put') as ud_p,
              patch('handlers.calculator.cf.lap_time') as lt,
              patch('handlers.calculator.user_language.get', new_callable=AsyncMock) as ul_g):
            lt.return_value = 'test_msg', 'test_keyboard'
            await calculator.lap_time_get(self.mock_message)
            ud_p.assert_called_once_with(12345, 'calculator', (False, True, False))
            ul_g.assert_called_once_with(12345)
            lt.assert_called_once()
            self.mock_message.answer.assert_called_once()


    async def test_race_time_get(self):
        '''тест сообщения, которое просит указать длительность гонки'''
        with (patch('handlers.calculator.user_data.put') as ud_p,
              patch('handlers.calculator.cf.race_duration') as rd,
              patch('handlers.calculator.user_language.get', new_callable=AsyncMock) as ul_g):
            rd.return_value = 'test_msg', 'test_keyboard'
            await calculator.race_time_get(self.mock_message)
            ud_p.assert_called_once_with(12345, 'calculator', (False, False, True))
            ul_g.assert_called_once_with(12345)
            rd.assert_called_once()
            self.mock_message.answer.assert_called_once()


    async def test_aprox_info_get_without_track(self):
        '''тест сообщения примерного калькулятора без выбранного трека'''
        with (patch('handlers.calculator.user_data.put') as ud_p,
              patch('handlers.calculator.user_data.get') as ud_g,
              patch('handlers.calculator.user_selection.get') as us_g,
              patch('handlers.calculator.user_language.get', new_callable=AsyncMock) as ul_g,
              patch('handlers.calculator.cf.aprox_builder') as ab):
            us_g.return_value = None
            ab.return_value = 'test_message', 'test_keyboard'
            await calculator.aprox_info_get(self.mock_message)
            ud_p.assert_called_once_with(12345, 'calculator', (False, False, False))
            ud_g.assert_called_once_with(12345, 'race_time')
            us_g.assert_called_once_with(12345, 'track')
            ul_g.assert_called_once_with(12345)
            ab.assert_called_once()
            self.mock_message.answer.assert_called_once()


    async def test_aprox_info_get_with_track_without_flow_and_time(self):
        '''тест сообщения примерного калькулятора с выбранным треком, но без данных по треку'''
        with (patch('handlers.calculator.user_data.put') as ud_p,
              patch('handlers.calculator.user_data.get') as ud_g,
              patch('handlers.calculator.user_selection.get') as us_g,
              patch('handlers.calculator.user_language.get', new_callable=AsyncMock) as ul_g,
              patch('handlers.calculator.DB_func.select_aprox_data', new_callable=AsyncMock) as sad,
              patch('handlers.calculator.cf.aprox_calc_builder') as acb):
            ud_g.return_value = 'test_race_time'
            acb.return_value = 'test_message', 'test_keyboard'
            us_g.return_value = 'test_track'
            sad.return_value = None, None
            await calculator.aprox_info_get(self.mock_message)
            ud_p.assert_called_once_with(12345, 'calculator', (False, False, False))
            ud_g.assert_called_once_with(12345, 'race_time')
            us_g.assert_called_once_with(12345, 'track')
            ul_g.assert_called_once_with(12345)
            sad.assert_called_once_with('test_track')
            acb.assert_called_once()
            self.mock_message.answer.assert_called_once()


    async def test_aprox_info_get_with_track_with_flow_and_time(self):
        '''тест сообщения примерного калькулятора с выбранным треком и с данными по треку'''
        with (patch('handlers.calculator.user_data.put') as ud_p,
              patch('handlers.calculator.user_data.get') as ud_g,
              patch('handlers.calculator.user_selection.get') as us_g,
              patch('handlers.calculator.user_language.get', new_callable=AsyncMock) as ul_g,
              patch('handlers.calculator.DB_func.select_aprox_data', new_callable=AsyncMock) as sad,
              patch('handlers.calculator.cf.aprox_builder') as ab):
            ud_g.return_value = 'test_race_time'
            ab.return_value = 'test_message', 'test_keyboard'
            us_g.return_value = 'test_track'
            sad.return_value = 'test_time', 'test_flow'
            await calculator.aprox_info_get(self.mock_message)
            ud_p.assert_called_once_with(12345, 'calculator', (False, False, False))
            ud_g.assert_called_once_with(12345, 'race_time')
            us_g.assert_called_once_with(12345, 'track')
            ul_g.assert_called_once_with(12345)
            sad.assert_called_once_with('test_track')
            ab.assert_called_once()
            self.mock_message.answer.assert_called_once()


    async def test_handler_all_mess_flowlap_valid(self):
        '''тест хендлера массового перехвата сообщений, когда в него прилетает валидный расход топлива на круг'''
        with (patch('handlers.calculator.user_language.get', new_callable=AsyncMock) as ul_g,
              patch('handlers.calculator.user_data.get') as ud_g,
              patch('handlers.calculator.cf.flow_read') as fr,
              patch('handlers.calculator.user_data.put') as ud_p,
              patch('handlers.calculator.accure_info_get') as aig):
            ud_g.return_value = (True, False, False)
            fr.return_value = 0.0
            with self.assertRaises(SkipHandler):
                await calculator.handler_all_mess(self.mock_message)
            ul_g.assert_called_once_with(12345)
            ud_g.assert_called_once_with(12345, 'calculator')
            fr.assert_called_once_with('test_text')
            ud_p.assert_called_once_with(12345, 'fuel_flow', 0.0)
            aig.assert_called_once_with(self.mock_message)


    async def test_handler_all_mess_flowlap_no_valid(self):
        '''тест хендлера массового перехвата сообщений, когда в него прилетает невалидный расход топлива на круг'''
        with (patch('handlers.calculator.user_language.get', new_callable=AsyncMock) as ul_g,
              patch('handlers.calculator.user_data.get') as ud_g,
              patch('handlers.calculator.messages.abort_flow') as af,
              patch('handlers.calculator.cf.flow_read', side_effect=ValueError) as fr):
            ud_g.return_value = (True, False, False)
            ul_g.return_value = 'RUS'
            with self.assertRaises(SkipHandler):
                await calculator.handler_all_mess(self.mock_message)
            ul_g.assert_called_once_with(12345)
            ud_g.assert_called_once_with(12345, 'calculator')
            fr.assert_called_once_with('test_text')
            af.assert_called_once_with('RUS')
            self.mock_message.answer.assert_called_once()


    async def test_handler_all_mess_laptime_valid(self):
        '''тест хендлера массового перехвата сообщений, когда в него прилетает валидное время круга'''
        with (patch('handlers.calculator.user_language.get', new_callable=AsyncMock) as ul_g,
              patch('handlers.calculator.user_data.get') as ud_g,
              patch('handlers.calculator.user_data.put') as ud_p,
              patch('handlers.calculator.cf.laptime_read') as lr,
              patch('handlers.calculator.accure_info_get') as aig):
            ud_g.return_value = (False, True, False)
            lr.return_value = timedelta(seconds=0)
            with self.assertRaises(SkipHandler):
                await calculator.handler_all_mess(self.mock_message)
            ul_g.assert_called_once_with(12345)
            ud_g.assert_has_calls([call(12345, 'calculator'), call(12345, 'calculator')])
            lr.assert_called_once_with('test_text')
            ud_p.assert_called_once_with(12345, 'lap_time', timedelta(seconds=0))
            aig.assert_called_once_with(self.mock_message)


    async def test_handlers_all_mess_laptime_no_vaild(self):
        '''тест хендлера массового перехвата сообщений, когда в него прилетает невалидное время круга'''
        with (patch('handlers.calculator.user_language.get', new_callable=AsyncMock) as ul_g,
              patch('handlers.calculator.user_data.get') as ud_g,
              patch('handlers.calculator.messages.abort_lap_time') as alt,
              patch('handlers.calculator.cf.laptime_read', side_effect=ValueError) as lr):
            ud_g.return_value = (False, True, False)
            ul_g.return_value = 'RUS'
            with self.assertRaises(SkipHandler):
                await calculator.handler_all_mess(self.mock_message)
            ul_g.assert_called_once_with(12345)
            ud_g.assert_has_calls([call(12345, 'calculator'), call(12345, 'calculator')])
            lr.assert_called_once_with('test_text')
            alt.assert_called_once_with('RUS')
            self.mock_message.answer.assert_called_once()


    async def test_handlers_all_mess_raceduration_valid_with_accure_mod(self):
        '''тест хендлера массового перехвата сообщений, когда в него
        прилетает валидная длительность гонки, под точный режим'''
        with (patch('handlers.calculator.user_language.get', new_callable=AsyncMock) as ul_g,
              patch('handlers.calculator.user_data.put') as ud_p,
              patch('handlers.calculator.user_data.get', side_effect=[(False, False, True),
                                                                            (False, False, True),
                                                                            (False, False, True),
                                                                            True]) as ud_g,
              patch('handlers.calculator.cf.duration_race') as dr,
              patch('handlers.calculator.accure_info_get') as aig):
            dr.return_value = timedelta(seconds=0)
            with self.assertRaises(SkipHandler):
                await calculator.handler_all_mess(self.mock_message)
            ul_g.assert_called_once_with(12345)
            ud_g.assert_has_calls([call(12345, 'calculator'),
                                   call(12345, 'calculator'),
                                   call(12345, 'calculator'),
                                   call(12345, 'accure')])
            dr.assert_called_once_with('test_text')
            ud_p.assert_called_once_with(12345, 'race_time', timedelta(seconds=0))
            aig.assert_called_once_with(self.mock_message)


    async def test_handlers_all_mess_raceduration_valid_with_aprox_mod(self):
        '''тест хендлера массового перехвата сообщений, когда в него
        прилетает валиданая длительность гонки под примерный режим'''
        with (patch('handlers.calculator.user_language.get', new_callable=AsyncMock) as ul_g,
              patch('handlers.calculator.user_data.put') as ud_p,
              patch('handlers.calculator.user_data.get', side_effect=[(False, False, True),
                                                                            (False, False, True),
                                                                            (False, False, True),
                                                                            False]) as ud_g,
              patch('handlers.calculator.cf.duration_race') as dr,
              patch('handlers.calculator.aprox_info_get') as aig):
            dr.return_value = timedelta(seconds=0)
            with self.assertRaises(SkipHandler):
                await calculator.handler_all_mess(self.mock_message)
            ul_g.assert_called_once_with(12345)
            ud_g.assert_has_calls([call(12345, 'calculator'),
                                   call(12345, 'calculator'),
                                   call(12345, 'calculator'),
                                   call(12345, 'accure')])
            dr.assert_called_once_with('test_text')
            ud_p.assert_called_once_with(12345, 'race_time', timedelta(seconds=0))
            aig.assert_called_once_with(self.mock_message)


    async def test_handlers_all_receduration_novalid(self):
        '''тест хендлера массового перехвата сообщений, когда в него
        прилетает невалидная длительность гонки'''
        with (patch('handlers.calculator.user_language.get', new_callable=AsyncMock) as ul_g,
              patch('handlers.calculator.user_data.get') as ud_g,
              patch('handlers.calculator.cf.duration_race', side_effect=ValueError) as dr,
              patch('handlers.calculator.messages.abort_race_duration') as ard):
            ud_g.return_value = (False, False, True)
            ul_g.return_value = 'RUS'
            with self.assertRaises(SkipHandler):
                await calculator.handler_all_mess(self.mock_message)
            ul_g.assert_called_once_with(12345)
            ud_g.assert_has_calls([call(12345, 'calculator'),
                                   call(12345, 'calculator'),
                                   call(12345, 'calculator')])
            dr.assert_called_once_with('test_text')
            ard.assert_called_once_with('RUS')
            self.mock_message.answer.assert_called_once()


    async def test_handlers_all_mess_track_select_with_valid_data(self):
        '''тест хендлера массового перехвата сообщений, когда в него
        прилетает название трека из примерного калькулятора'''
        with (patch('handlers.calculator.user_language.get', new_callable=AsyncMock) as ul_g,
              patch('handlers.calculator.user_selection.put') as us_p,
              patch('handlers.calculator.user_selection.get') as us_g,
              patch('handlers.calculator.user_data.get', side_effect=[(False, False, False),
                                                                            (False, False, False),
                                                                            (False, False, False),
                                                                            True]) as ud_g,
              patch('handlers.calculator.aprox_info_get') as aig):
            self.mock_message.text = '/test_text'
            with self.assertRaises(SkipHandler):
                await calculator.handler_all_mess(self.mock_message)
            ul_g.assert_called_once_with(12345)
            ud_g.assert_has_calls([call(12345, 'calculator'),
                                   call(12345, 'calculator'),
                                   call(12345, 'calculator'),
                                   call(12345, 'calculator_works')])
            us_g.assert_called_once_with(12345, 'track_selector')
            us_p.assert_has_calls([call(12345, 'track_selector', False),
                                   call(12345, 'track', '/test_text')])
            aig.assert_called_once_with(self.mock_message)


    async def test_handlers_all_mess_track_select_wtih_no_valid_data(self):
        '''текст хендлера массового перехвата сообщений, когда в него
        прилетает не валидное название трека из переменного калькулятора'''
        with (patch('handlers.calculator.user_language.get', new_callable=AsyncMock) as ul_g,
              patch('handlers.calculator.user_selection.put') as us_p,
              patch('handlers.calculator.user_selection.get') as us_g,
              patch('handlers.calculator.user_data.get') as ud_g):
            self.mock_message.text = 'test_text'
            ud_g.return_value = (False, False, False)
            with self.assertRaises(SkipHandler):
                await calculator.handler_all_mess(self.mock_message)
            ul_g.assert_called_once_with(12345)
            ud_g.assert_has_calls([call(12345, 'calculator'),
                                   call(12345, 'calculator'),
                                   call(12345, 'calculator')])
            us_g.assert_called_once_with(12345, 'track_selector')
            us_p.assert_called_once_with(12345, 'track_selector', False)


    async def test_handlers_all_mess_track_select_wtih_valid_data_calculator_is_not_work(self):
        '''тест хендлера массового перехвата сообщений, когда в него
        прилетает название трека из примерного калькулятора'''
        with (patch('handlers.calculator.user_language.get', new_callable=AsyncMock) as ul_g,
              patch('handlers.calculator.user_selection.put') as us_p,
              patch('handlers.calculator.user_selection.get') as us_g,
              patch('handlers.calculator.user_data.get', side_effect=[(False, False, False),
                                                                            (False, False, False),
                                                                            (False, False, False),
                                                                            False]) as ud_g,
              patch('handlers.calculator.aprox_info_get') as aig):
            self.mock_message.text = '/test_text'
            with self.assertRaises(SkipHandler):
                await calculator.handler_all_mess(self.mock_message)
            ul_g.assert_called_once_with(12345)
            ud_g.assert_has_calls([call(12345, 'calculator'),
                                   call(12345, 'calculator'),
                                   call(12345, 'calculator'),
                                   call(12345, 'calculator_works')])
            us_g.assert_called_once_with(12345, 'track_selector')
            us_p.assert_has_calls([call(12345, 'track_selector', False),
                                   call(12345, 'track', '/test_text')])



