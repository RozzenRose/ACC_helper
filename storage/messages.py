start_message_letter = (f'Привет, это бот-помошник для игры Asetto Corsa Competizione!\n\n'
                        f'Для того чтобы получить сетапы или трекгайды, сначала нужно выбрать трассу и автомобиль.\n\n'
                        f'Для того что бы применить сетапы к машине, открой архив и помести файлы из него в:\n '
                        f'___C:\\users\\username\\Assetto Corsa Competizione\\Setups\\папка машины\\папка трассы___\n\n')
start_message_letter_en = (f'Hello! It is bot-helper for the Asetto Corsa Competizione!\n\n'
                           f'Choose your car and track for get track guide and setups.\n\n'
                           f'For use setups open a archiv whit setups and moove files in:\n '
                           f'___C:\\users\\username\\Assetto Corsa Competizione\\Setups\\car folder\\track folder___\n\n')

car_select_message = (f'Выбери машину:\n\n'
                        f'Porsche:\n'
                        f'/Porsche_922_GT3R\n'
                        f'Ferrari:\n'
                        f'/Ferrari_296_GT3\n'
                        f'Lamborghini:\n'
                        f'/Lamborghini_Huracan_GT3_EVO_2\n\n')
car_select_message_en = (f'Select a car:\n\n'
                        f'Porsche:\n'
                        f'/Porsche_922_GT3R\n'
                        f'Ferrari:\n'
                        f'/Ferrari_296_GT3\n'
                        f'Lamborghini:\n'
                        f'/Lamborghini_Huracan_GT3_EVO_2\n\n')

track_select_message = (f'Выбери трассу:\n'
                        f'/Spa_Francorchamps\n'
                        f'/Monza\n'
                        f'/Misano')
track_select_message_en = (f'Select a track:\n'
                        f'/Spa_Francorchamps\n'
                        f'/Monza\n'
                        f'/Misano')

calculator_selector = ('При примерном расчете, бот посчитает топливо исходя из примерного расхода топлива на круг и премерного времени круга для указанной трассы на автоиобиле класса GT3\n\n'
                       'При точном расчете будет необходимо указать ваш средний расход топлива на круг, а так же ваше среднее время круга\n')
calculator_selector_en = ('With an approximate calculation, the bot will calculate the fuel based on the approximate fuel consumption per lap and the approximate lap time for the specified track on a GT3 class car\n\n'
                          'For an accurate calculation, you will need to indicate your average fuel consumption per lap, as well as your average lap time.')

def accurate_calculator(fuel_flow, lap_time, race_time, answer):
    return (f'Введи неоходимые данные для расчета топлива! \n'
            f'Любой параметр можно указать заного\n\n'
            f'Текущие данные:\n\n'
            f'Расход топлива на круг: \n'
            f'*{fuel_flow if fuel_flow is not None else "НЕТ ДАННЫХ"}* литров на круг\n\n'
            f'Среднее вермя круга: \n'
            f'*{int(lap_time.total_seconds() // 60) if lap_time is not None else 'НЕТ ДАННЫХ'}* минут \n'
            f'*{lap_time.seconds - (int(lap_time.total_seconds() // 60) * 60) if lap_time is not None else 'НЕТ ДАННЫХ'}* секунд \n'
            f'*{str(lap_time.total_seconds()).split('.')[1].ljust(3, '0') if lap_time is not None else 'НЕТ ДАННЫХ'}* миллисекунды \n\n'
            f'Общее время гонки: \n'
            f'{int(race_time.total_seconds() // 3600) if race_time is not None else 'НЕТ ДАННЫХ'} часов \n'
            f'{round(int(race_time.total_seconds() // 60) - (int(race_time.total_seconds() // 3600) * 60), 3) if race_time is not None else 'НЕТ ДАННЫХ'} минут \n\n'
            f'На эту гонку нужно залить *{round(answer, 3) if race_time is not None else 'НЕТ ДАННЫХ'}* литров')
def accurate_calculator_en(fuel_flow, lap_time, race_time, answer):
    return (f'Enter the required data to calculate fuel!\n'
            f'Any parameter can be specified again\n\n'
            f'Current data:\n\n'
            f'Fuel consumption per circle: \n'
            f'*{fuel_flow if fuel_flow is not None else 'NO DATA'}* liters per lap\n\n'
            f'Average lap time: \n'
            f'*{int(lap_time.total_seconds() // 60) if lap_time is not None else 'NO DATA'}* minutes \n'
            f'*{lap_time.seconds - (int(lap_time.total_seconds() // 60) * 60) if lap_time is not None else 'NO DATA'}* seconds \n'
            f'*{str(lap_time.total_seconds()).split('.')[1].ljust(3, '0') if lap_time is not None else 'NO DATA'}* milliseconds \n\n'
            f'Race duration: \n'
            f'*{int(race_time.total_seconds() // 3600) if race_time is not None else 'NO DATA'}* hours \n'
            f'*{round(int(race_time.total_seconds() // 60) - (int(race_time.total_seconds() // 3600) * 60), 3) if race_time is not None else 'NO DATA'}* minutes \n\n'
            f'You will need *{round(answer, 3) if race_time is not None else 'NO DATA'}* liters')

get_flow = f'Введи средний расход топлива на круг, десятые отдели точкой:'
get_flow_en = f'Enter the average fuel consumption per lap, separating tenths with a dot:'

get_lap_time = (f'Введи среднее время круга в формате `Min:Sec:Mic` : \n'
                f'Если твой круг меньше минуты, используй формат `Sec:Mic`')
get_lap_time_en = (f'Enter average lap time in `Min:Sec:Mic` format: \n'
                   f'If your lap time is less than a minute just use `Sec:Mic` format:')

get_race_duration = (f'Бот понимает форматы `Hour:Min` или просто `Min`')
get_race_duration_en = (f'You can use formats `Hour:Min` or `Min`')

abort_flow = (f'То что ты ввел не получилось преобразовать в число, попробуй еще раз\n\n'
              f'Введи средний расход топлива на круг, десятые отдели точкой:')
abort_flow_en = (f'What you entered could not be converted into a number, try again\n\n'
                 f'Enter the average fuel consumption per lap, separating tenths with a dot:')

abort_lap_time = (f'То что ты ввел не получилось преобразовать во время \n \n'
                  f'Введи среднее время круга в формате `Min:Sec:Mic` : \n'
                  f'Если твой круг меньше минуты, пиши просто `Sec:Mic`')
abort_lap_time_en = (f'What you entered could not be converted into time lap, try again \n \n'
                     f'Use `Min:Sec:Mic` format: \n'
                     f'If your lap time is less than a minute just use `Sec:Mic` format')

abort_race_duration = (f'То что ты ввел не получилось преобрзовать во вреся продолжительности гонки\n\n'
                                     f'Бот понимает форматы `Hour:Min` или просто `Min`')
abort_race_duration_en = (f'What you entered could not be convert inte time of race duration\n\n'
                          f'Use `Hour:Min` or `Min` formats')