from datetime import timedelta
import math

class Data:
    def __new__(cls, *arg, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def put(self, user_id, key, value):
        if user_id not in self.data:
            self.data[user_id] = {}
        self.data[user_id][key] = value

    def get(self, user_id, key=None):
        user_data = self.data.get(user_id, {})
        if key:
            return user_data.get(key, None)
        return user_data

    def forget_all(self, user_id):
        if user_id in self.data:
            del self.data[user_id]


class UserSelection(Data):
    data = {}
    _instance = None

    def __init__(self, user_id=None):
        if user_id not in self.data:
            if user_id is not None:
                self.data[user_id] = {
                    'car_selector': False,  # активирован режив выбора машины
                    'car': None,  # машина
                    'track_selector': False,  # активирован режим выбора трассы
                    'track': None}  # трек


class UserData(Data):
    data = {}
    _instance = None

    def __init__(self, user_id=None):
        if user_id not in self.data:
            if user_id is not None:
                self.data[user_id] = {
                    'calculator_works': False,  # флаг работы калькулятора
                    'calculator': (False, False, False),  # шаги алгортима рассчета топлива для точного калькулятора
                    'fuel_flow': None,  # расход топлива на круг
                    'lap_time': None,  # время круга
                    'race_time': None,  # время гонки
                    'accure': False}  # точный / примерный


class LanguageSelect(Data):
    user_language = {}
    _instance = None

    def __init__(self, user_id=None):
        if user_id not in self.user_language:
            if user_id is not None:
                self.user_language[user_id] = None

    def put(self, user_id, value):
        self.user_language[user_id] = value

    def get(self, user_id):
        user_data = self.user_language.get(user_id, 'ENG')
        return user_data


user_language = LanguageSelect()
user_data = UserData()
user_selection = UserSelection()


def accurate_calculation(fuel_flow: float, lap_time: timedelta, race_time: timedelta) -> float:
    if None in (fuel_flow, lap_time, race_time):
        return None
    return (math.ceil(race_time // lap_time)) * fuel_flow
