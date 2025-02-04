from datetime import timedelta

class UserSelection:
    data = {}
    _instance = None

    def __new__(cls, *arg, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, user_id=None):
        if user_id not in self.data:
            if user_id is not None:
                self.data[user_id] = {
                'car_selector': False,                #активирован режив выбора машины
                'car': None,                          #машина
                'track_selector': False,              #активирован режим выбора трассы
                'track': None}                        #трек

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

user_selection = UserSelection()

class UserData:
    data = {}
    _instance = None

    def __new__(cls, *arg, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, user_id=None):
        if user_id not in self.data:
            if user_id is not None:
                self.data[user_id] = {
                'calculator_works': False,            #флаг работы калькулятора
                'calculator': (False, False, False),  #шаги алгортима рассчета топлива для точного калькулятора
                'fuel_flow': None,                    #расход топлива на круг
                'lap_time': None,                     #время круга
                'race_time': None}                    #время гонки


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

user_data = UserData()

class FuelCalculator:
    @staticmethod
    def accurate_calculation(fuel_flow: float, lap_time: timedelta, race_time: timedelta) -> float:
        if None in (fuel_flow, lap_time, race_time):
            return 'НЕТ ДАННЫХ'
        return (int(race_time//lap_time) + 1) * fuel_flow

    @staticmethod
    def approximate_calculation():
        pass