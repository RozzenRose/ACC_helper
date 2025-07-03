import unittest
from unittest.mock import call
from unittest.mock import AsyncMock, patch
from aiogram.types import Message, User
from handlers import main_root
from aiogram.dispatcher.event.bases import SkipHandler


class TestMainRoot(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        '''Инициализация мок-объектов перед каждым тестом'''
        self.mock_message = AsyncMock(spec=Message)
        self.mock_message.from_user = User(id=12345, username='test_user', is_bot=False, first_name="Test")
        self.mock_message.answer = AsyncMock()
        self.mock_message.answer_document = AsyncMock()
        self.mock_message.text = 'test_text'


    async def test_cmd_start_with_lang(self):
        '''Тестируем обработчик /start, язык выбран'''
        with (patch('handlers.functions.main_root_functions.user_initialization') as mock_init,
              patch('custom_classes.user_language.get') as get_lan,
              patch('handlers.functions.main_root_functions.start_message') as start_builder,
              patch('custom_classes.user_selection.get') as get_data):
            mock_init.return_value = None  # Заглушка инициализации пользователя
            get_lan.return_value = 'RUS' # язык выбран, какой не важно
            start_builder.return_value = ('text', 'keyboard') # ответ билдера сообщений
            await main_root.cmd_start(self.mock_message)
            mock_init.assert_called_once_with(12345) # Проверяем, что user_initialization вызвана
            get_lan.assert_called_once_with(12345) # Проверяем, что была вызвана проверка языка
            get_data.assert_has_calls([call(12345, 'track'), call(12345, 'car')], any_order=True)
            start_builder.assert_called_once_with(get_data(12345, 'car'), get_data(12345, 'track'), 'RUS')
            self.mock_message.answer.assert_called_once() # Проверяем, что сообщение отправлено


    async def test_cmd_start_without_lang(self):
        '''Тестируем обработчик /start, язык не выбран'''
        with (patch('handlers.functions.main_root_functions.user_initialization') as mock_init,
              patch('custom_classes.user_language.get') as get_lan,
              patch('handlers.functions.main_root_functions.lang_select_message') as select_message):
            mock_init.return_value = None  # Заглушка инициализации пользователя
            get_lan.return_value = None # Язык не выбран
            select_message.return_value = ('text', 'keyboard') #ответ билдера сообщений
            await main_root.cmd_start(self.mock_message)
            mock_init.assert_called_once_with(12345) # Проверяем, что user_initialization вызвана
            get_lan.assert_called_once_with(12345) # Проверяем, что была вызвана проверка языка
            select_message.assert_called_once() # Проверяем, что была вызвана функция сборки сообщения для выбора языка
            self.mock_message.answer.assert_called_once() # Проверяем, что сообщение отправлено


    async def test_select_eng(self):
        '''Проверяем выбор английского языка'''
        with (patch('custom_classes.user_language.put', new_callable=AsyncMock) as mock_db_put,
              patch('handlers.main_root.cmd_start', new_callable=AsyncMock) as mock_cmd_start):
            await main_root.select_eng(self.mock_message)
            mock_db_put.assert_called_once_with(12345, 'test_user', 'ENG') # Проверяем, что язык сохранен
            mock_cmd_start.assert_called_once_with(self.mock_message) # Проверяем, что управление улетает в стартовый хендлер


    async def test_select_rus(self):
        '''Проверяем выбор русского языка'''
        with (patch('custom_classes.user_language.put', new_callable=AsyncMock) as mock_db_put,
              patch('handlers.main_root.cmd_start', new_callable=AsyncMock) as mock_cmd_start):
            await main_root.select_rus(self.mock_message)
            mock_db_put.assert_called_once_with(12345, 'test_user', 'RUS') # Проверяем вызов user_language.put()
            mock_cmd_start.assert_called_once_with(self.mock_message) # Проверяем вызов cmd_start()


    async def test_lan_swap_to_eng(self):
        '''Проверяем функцию смены языка c русского на английский'''
        with (patch('custom_classes.user_language.get', new_callable=AsyncMock) as get_mock,
              patch('custom_classes.user_language.put', new_callable=AsyncMock) as put_mock,
              patch('handlers.main_root.cmd_start', new_callable=AsyncMock) as start_mock):
            get_mock.return_value = 'RUS' # сейчас мы на русском, а переключаемся на английский
            await main_root.lan_swap(self.mock_message)
            get_mock.assert_called_once_with(12345) # проверка получения языка
            put_mock.assert_called_once_with(12345, 'test_user', 'ENG') # проверка вызова запоминания языка
            start_mock.assert_called_once_with(self.mock_message) # Проверка вызова cmd_start()


    async def test_lan_swap_to_rus(self):
        '''Проверяем функцию смены языка c английского на русский'''
        with (patch('custom_classes.user_language.get', new_callable=AsyncMock) as get_mock,
              patch('custom_classes.user_language.put', new_callable=AsyncMock) as put_mock,
              patch('handlers.main_root.cmd_start', new_callable=AsyncMock) as start_mock):
            get_mock.return_value = 'ENG' # сейчас мы на английском, а переключаемся на русский
            await main_root.lan_swap(self.mock_message)
            get_mock.assert_called_once_with(12345) # проверка получения языка
            put_mock.assert_called_once_with(12345, 'test_user', 'RUS') # проверка вызова запоминания языка
            start_mock.assert_called_once_with(self.mock_message) # проверка вызова cmd_start()


    async def test_cache_drop(self):
        '''Првоеряем функцию сброса кеша на русском языке'''
        with (patch('handlers.main_root.mrf.delete_cache') as del_c,
              patch('handlers.main_root.cmd_start', new_callable=AsyncMock) as start_mock):
            await main_root.caсhe_drop(self.mock_message)
            del_c.assert_called_once_with(12345) #проверка вызова функции сброса кэша
            start_mock.assert_called_once_with(self.mock_message) # проверка вызова cmd_start()


    async def test_reboot(self):
        '''Проверка работы кнопки "⬅️ В начало"'''
        with (patch('handlers.main_root.mrf.delete_selection') as del_sel,
              patch('handlers.main_root.cmd_start', new_callable=AsyncMock) as start_mock):
            await main_root.reboot(self.mock_message)
            del_sel.assert_called_once_with(12345) #проверка функции сброса пользовательских выборов
            start_mock.assert_called_once_with(self.mock_message) # проверка вызова cmd_start()


    async def test_car_selector(self):
        '''Тест функции выбора машины'''
        with (patch('handlers.main_root.user_selection.put') as sel_put,
              patch('handlers.main_root.messages.car_select_message') as csm,
              patch('handlers.main_root.user_language.get', new_callable=AsyncMock) as lan_get):
            await main_root.car_selector(self.mock_message)
            sel_put.assert_has_calls([call(12345, 'track_selector', False),
                                     call(12345, 'car_selector', True)],
                                     any_order=True)
            csm.assert_called_once_with(await lan_get(12345))
            self.mock_message.answer.assert_called_once()  # Проверяем, что сообщение отправлено


    async def test_track_selector(self):
        '''Тест функции выбора трассы'''
        with (patch('handlers.main_root.user_selection.put') as sel_put,
              patch('handlers.main_root.messages.track_select_message') as tsm,
              patch('handlers.main_root.user_language.get', new_callable=AsyncMock) as lan_get):
            await main_root.track_selector(self.mock_message)
            sel_put.assert_has_calls([call(12345, 'track_selector', True),
                                      call(12345, 'car_selector', False)],
                                      any_order=True)
            tsm.assert_called_once_with(await lan_get(12345))
            self.mock_message.answer.assert_called_once()  # Проверяем, что сообщение отправлено


    async def test_track_guide_wtihot_selection(self):
        '''Тест получения трекгайда при невыбранной трассе или машине'''
        with (patch('handlers.main_root.user_selection.get') as us_g,
              patch('handlers.main_root.cmd_start') as start_message):
            us_g.return_value = None
            with self.assertRaises(SkipHandler):
                await main_root.track_guide(self.mock_message)
            us_g.assert_has_calls([call(12345, 'car'), call(12345, 'track')], any_order=True)
            start_message.assert_called_once_with(self.mock_message)


    async def test_track_guide_with_selection_track(self):
        '''Тест получения трекгайда при выбранной трассе или машине, при том, что гайд есть'''
        with (patch('handlers.main_root.user_selection.get') as us_g,
              patch('handlers.main_root.mrf.trackguide_select') as ts,
              patch('handlers.main_root.cmd_start') as start_message):
            us_g.return_value = 'test_return'
            ts.return_value = 'URL'
            await main_root.track_guide(self.mock_message)
            ts.assert_called_once_with('test_return', 'test_return')
            self.mock_message.answer.assert_called_once_with('URL')


    async def test_track_guide_with_selection_notrack(self):
        '''Тест получения трекгайда при выбранной трассе или машине, при том, что гайда нет'''
        with (patch('handlers.main_root.user_selection.get') as us_g,
              patch('handlers.main_root.mrf.trackguide_select') as ts,
              patch('handlers.main_root.user_language.get', new_callable=AsyncMock) as l_get,
              patch('handlers.main_root.messages.fail_tg') as fail_tg):
            us_g.return_value = 'test_return'
            ts.return_value = ''
            await main_root.track_guide(self.mock_message)
            ts.assert_called_once_with('test_return', 'test_return')
            l_get.assert_called_once_with(12345)
            fail_tg.assert_called_once()
            self.mock_message.answer.assert_called_once()


    async def test_setup_without_selection(self):
        '''Тест получения сетапа, без выбранных машины и трассы'''
        with (patch('handlers.main_root.user_selection.get') as us_g,
              patch('handlers.main_root.cmd_start') as start_message):
            us_g.return_value = None
            with self.assertRaises(SkipHandler):
                await main_root.track_guide(self.mock_message)
            start_message.assert_called_once_with(self.mock_message)


    async def test_setup_with_selection_file(self):
        '''Тест получения сетапа с выбранными машиной и трассой, и с существующим файлом'''
        with (patch('handlers.main_root.user_selection.get') as us_g,
              patch('handlers.main_root.os.path.isfile') as file_exists,
              patch('handlers.main_root.FSInputFile') as FSIF):
            us_g.return_value = 'test_answer'
            file_exists.return_value = True
            await main_root.setup(self.mock_message)
            us_g.assert_has_calls([call(12345, 'car'), call(12345, 'track')], any_order=True)
            FSIF.assert_called_once()
            self.mock_message.answer_document.assert_called_once()


    async def test_setup_with_selection_nofile(self):
        '''Тест получения сетапа с выбранными машиной и трассой, и файл не существует'''
        with (patch('handlers.main_root.user_selection.get') as us_g,
              patch('handlers.main_root.os.path.isfile') as file_exists,
              patch('handlers.main_root.user_language.get', new_callable=AsyncMock) as lang_get,
              patch('handlers.main_root.messages.fail_setup') as fail_setup):
            us_g.return_value = 'test_answer'
            file_exists.return_value = False
            await main_root.setup(self.mock_message)
            us_g.assert_has_calls([call(12345, 'car'), call(12345, 'track')], any_order=True)
            file_exists.assert_called_once()
            lang_get.assert_called_once_with(12345)
            fail_setup.assert_called_once()
            self.mock_message.answer.assert_called_once()


    async def test_handler_selector_cs_with_valid_msg(self):
        '''тест хендлера общего перехвата, при валидном сообщении с машиной'''
        with (patch('handlers.main_root.user_selection.get') as cs,
              patch('handlers.main_root.mrf.car_selection') as car_s,
              patch('handlers.main_root.mrf.reset_select') as rs,
              patch('handlers.main_root.cmd_start') as start_message):
            cs.return_value = True
            car_s.return_value = True
            await main_root.handler_selector(self.mock_message)
            cs.assert_called_once_with(12345, 'car_selector')
            car_s.assert_called_once_with(12345, 'test_text')
            rs.assert_called_once()
            start_message.assert_called_once_with(self.mock_message)


    async def test_handler_selector_cs_without_valid_msg(self):
        '''тест хендлера общего перехвата, при не валидном сообщении с машиной'''
        with (patch('handlers.main_root.user_selection.get') as cs,
              patch('handlers.main_root.mrf.car_selection') as car_s):
            cs.return_value = True
            car_s.return_value = False
            with self.assertRaises(SkipHandler):
                await main_root.handler_selector(self.mock_message)
            cs.assert_called_once_with(12345, 'car_selector')
            car_s.assert_called_once_with(12345, 'test_text')


    async def test_handler_selector_ts_with_valid_msg(self):
        '''тест хендлера общего перехвата, при валидном сообщении с треком'''
        with (patch('handlers.main_root.user_selection.get', side_effect=[False, True]) as ts,
              patch('handlers.main_root.mrf.track_selection') as track_s,
              patch('handlers.main_root.mrf.reset_select') as rs,
              patch('handlers.main_root.cmd_start') as start_message):
            track_s.return_value = True
            await main_root.handler_selector(self.mock_message)
            ts.assert_has_calls([call(12345, 'car_selector'), call(12345, 'track_selector')])
            track_s.assert_called_once_with(12345, 'test_text')
            rs.assert_called_once()
            start_message.assert_called_once_with(self.mock_message)


    async def test_handler_selector_ts_without_valid_msg(self):
        '''тест хендлера общего перехвата, при не валидном сообщении с треком'''
        with (patch('handlers.main_root.user_selection.get', side_effect=[False, True]) as ts,
              patch('handlers.main_root.mrf.track_selection') as track_s):
            track_s.return_value = False
            with self.assertRaises(SkipHandler):
                await main_root.handler_selector(self.mock_message)
            ts.assert_has_calls([call(12345, 'car_selector'), call(12345, 'track_selector')])
            track_s.assert_called_once_with(12345, 'test_text')


    async def test_handler_selector_without_selections(self):
        '''тест освобожения сообщения из общего хендлера'''
        with (patch('handlers.main_root.user_selection.get', side_effect=[False, False]) as ts):
            with self.assertRaises(SkipHandler):
                await main_root.handler_selector(self.mock_message)
            ts.assert_has_calls([call(12345, 'car_selector'), call(12345, 'track_selector')])


if __name__ == "__main__":
    unittest.main()


