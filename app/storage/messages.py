def start_msg_placeholder(lang):
    if lang == 'RUS':
        return 'Чем займемся сегодня?'
    else:
        return 'What do you want to do?'


def calculator_msg_placeholder(lang):
    if lang == 'RUS':
        return 'Выбери тип калькулятора'
    else:
        return 'Select a type of calculator'


def start_message_letter(car, track, lang):
    if lang == 'RUS':
        return (f'Привет, это бот-помошник для игры Asetto Corsa Competizione!\n\n'
                f'Для того чтобы получить сетапы или трекгайды, сначала нужно выбрать трассу и автомобиль.\n\n'
                f'Для того что бы применить сетапы к машине, открой архив и помести файлы из него в:\n '
                f'___C:\\users\\username\\Assetto Corsa Competizione\\Setups\\папка машины\\папка трассы___\n\n'
                f'🏎️ Текущая машина:   *{car[1:] if car != None else "Нет выбранной машины"}*\n'
                f'🏁 Текущая трасса:   *{track[1:] if track != None else "Нет выбранной трассы"}*')
    else:
        return (f'Hello! It is bot-helper for the Asetto Corsa Competizione!\n\n'
                f'In order to get your track guide and setups, you need to choose your car and track:\n '
                f'In order to apply the setups to the car, open the archive and place the files from it into the path:\n'
                f'___C:\\users\\username\\Assetto Corsa Competizione\\Setups\\car folder\\track folder___\n\n'
                f'🏎️ Current car:   *{car[1:] if car != None else "No selected car"}*\n'
                f'🏁 Current track:   *{track[1:] if track != None else "No selected track"}*')


lang_select = (f'Select your language:\n'
               f'Выбери язык:')


def car_select_message(lang):
    if lang == 'RUS':
        return (f'Выбери машину:\n\n'
                f'Porsche:\n'
                f'/Porsche_922_GT3R\n'
                f'Ferrari:\n'
                f'/Ferrari_296_GT3\n'
                f'Lamborghini:\n'
                f'/Lamborghini_Huracan_GT3_EVO_2\n'
                f'BMW:\n'
                f'/BMW_M4_GT3\n'
                f'McLaren:\n'
                f'/McLaren_720s_EVO_GT3\n'
                f'Ford:\n'
                f'/Ford_Mustang_GT3\n'
                f'Aston Martin:\n'
                f'/Aston_Martin_V8_Vantage\n')
    else:
        return (f'Select a car:\n\n'
                f'Porsche:\n'
                f'/Porsche_922_GT3R\n'
                f'Ferrari:\n'
                f'/Ferrari_296_GT3\n'
                f'Lamborghini:\n'
                f'/Lamborghini_Huracan_GT3_EVO_2\n'
                f'BMW:\n'
                f'/BMW_M4_GT3\n'
                f'McLaren:\n'
                f'/McLaren_720s_EVO_GT3\n'
                f'Ford:\n'
                f'/Ford_Mustang_GT3\n'
                f'Aston Martin:\n'
                f'/Aston_Martin_V8_Vantage\n')


def track_select_message(lang):
    if lang == 'RUS':
        return (f'Выбери трассу:\n'
                f'/Spa_Francorchamps\n'
                f'/Monza\n'
                f'/Misano\n'
                f'/Hungaroring\n'
                f'/Watkins_Glen\n'
                f'/Mount_Panorama\n'
                f'/Imola\n'
                f'/Nur')
    else:
        return (f'Select a track:\n'
                f'/Spa_Francorchamps\n'
                f'/Monza\n'
                f'/Misano\n'
                f'/Hungaroring\n'
                f'/Watkins_Glen\n'
                f'/Mount_Panorama\n'
                f'/Imola\n'
                f'/Nur')


def calculator_selector(lang):
    if lang == 'RUS':
        return (
            'При примерном расчете, бот посчитает топливо исходя из примерного расхода топлива на круг и премерного времени круга для указанной трассы на автоиобиле класса GT3\n\n'
            'При точном расчете будет необходимо указать ваш средний расход топлива на круг, а так же ваше среднее время круга')
    else:
        return (
            'For an approximate calculation, the bot will calculate the fuel based on the approximate fuel consumption per lap and the approximate lap time for the specified track on a GT3 class car\n\n'
            'For an accurate calculation, you will need to indicate your average fuel consumption per lap, as well as your average lap time.')


def accurate_calculator(fuel_flow, lap_time, race_time, answer, lang):
    if lang == 'RUS':
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
                f'На эту гонку нужно залить *{round(answer, 3) if answer is not None else 'НЕТ ДАННЫХ'}* литров\n'
                f'Если предусмотрен разогревочный круг, залить нужно *{(round(answer, 3) + fuel_flow) if answer is not None else 'НЕТ ДАННЫХ'} литров*')
    else:
        return (f'Enter the required data to calculate fuel!\n'
                f'Any parameter can be specified again\n\n'
                f'Current data:\n\n'
                f'Fuel consumption per lap: \n'
                f'*{fuel_flow if fuel_flow is not None else 'NO DATA'}* liters per lap\n\n'
                f'Average lap time: \n'
                f'*{int(lap_time.total_seconds() // 60) if lap_time is not None else 'NO DATA'}* minutes \n'
                f'*{lap_time.seconds - (int(lap_time.total_seconds() // 60) * 60) if lap_time is not None else 'NO DATA'}* seconds \n'
                f'*{str(lap_time.total_seconds()).split('.')[1].ljust(3, '0') if lap_time is not None else 'NO DATA'}* milliseconds \n\n'
                f'Race duration: \n'
                f'*{int(race_time.total_seconds() // 3600) if race_time is not None else 'NO DATA'}* hours \n'
                f'*{round(int(race_time.total_seconds() // 60) - (int(race_time.total_seconds() // 3600) * 60), 3) if race_time is not None else 'NO DATA'}* minutes \n\n'
                f'You need to fill up *{round(answer, 3) if answer is not None else 'NO DATA'}* liters\n'
                f'If a warm-up circle is provided, you will need *{(round(answer, 3) + fuel_flow) if answer is not None else 'НЕТ ДАННЫХ'}* litres')


def get_flow(lang):
    if lang == 'RUS':
        return f'Введи средний расход топлива на круг, десятые отдели точкой:'
    else:
        return f'Enter the average fuel consumption per lap, separating tenths with a dot:'


def get_lap_time(lang):
    if lang == 'RUS':
        return (f'Введи среднее время круга в формате `Min:Sec:Mic` : \n'
                f'Если твой круг меньше минуты, используй формат `Sec:Mic`')
    else:
        return (f'Enter average lap time in `Min:Sec:Mic` format: \n'
                f'If your lap time is less than a minute just use `Sec:Mic` format:')


def get_race_duration(lang):
    if lang == 'RUS':
        return (f'Бот понимает форматы `Hour:Min` или просто `Min`')
    else:
        return (f'You can use formats `Hour:Min` or `Min`')


def abort_flow(lang):
    if lang == 'RUS':
        return (f'То что ты ввел не получилось преобразовать в число, попробуй еще раз\n\n'
                f'Введи средний расход топлива на круг, десятые отдели точкой:')
    else:
        return (f'What you entered could not be converted into a number, try again\n\n'
                f'Enter the average fuel consumption per lap, separating tenths with a dot:')


def abort_lap_time(lang):
    if lang == 'RUS':
        return (f'То что ты ввел не получилось преобразовать во время \n \n'
                f'Введи среднее время круга в формате `Min:Sec:Mic` : \n'
                f'Если твой круг меньше минуты, пиши просто `Sec:Mic`')
    else:
        return (f'What you entered could not be converted into time lap, try again \n \n'
                f'Use `Min:Sec:Mic` format: \n'
                f'If your lap time is less than a minute just use `Sec:Mic` format')


def abort_race_duration(lang):
    if lang == 'RUS':
        return (f'То что ты ввел не получилось преобрзовать во время продолжительности гонки\n\n'
                f'Бот понимает форматы `Hour:Min` или просто `Min`')
    else:
        return (f'What you entered could not be convert inte time of race duration\n\n'
                f'Use `Hour:Min` or `Min` formats')


def aprox_calculation(track, race_time, answer, lap_flow, lap_time, lang):
    if lang == 'RUS':
        return (f'Для примерного расчета топлива нужно указать трассу и длительность гонки. '
                f'Бот из примерных значений времени круга и расхода посчитает топливо. '
                f'Расчет будет очень примерным, не рекомендуем для важных заездов!\n\n'
                f'Выбранная трасса: {track[1:].replace('_', '\\_') if track is not None else 'НЕТ ДАННЫХ'}\n'
                f'Примерный расход на круг: {lap_flow if lap_flow is not None else 'НЕТ ДАННЫХ'}\n'
                f'Примерное время круга: {lap_time if lap_time is not None else 'НЕТ ДАННЫХ'}\n\n'
                f'Продолжительность гонки: \n'
                f'{int(race_time.total_seconds() // 3600) if race_time is not None else 'НЕТ ДАННЫХ'} часов\n'
                f'{round(int(race_time.total_seconds() // 60) - (int(race_time.total_seconds() // 3600) * 60), 3) if race_time is not None else 'НЕТ ДАННЫХ'} минут\n\n'
                f'Тебе нужно залить: {round(answer, 3) if answer is not None else 'НЕТ ДАННЫХ'} литров')
    else:
        return (f'To calculate the approximate fuel cost, you need to specify the route and duration of the race.\n\n '
                f'The bot will calculate fuel from approximate lap time and consumption values.\n\n '
                f'The calculation will be very approximate, not recommended for important races!\n\n'
                f'Selected route: {track[1:].replace('_', '\\_') if track is not None else 'NO DATA'}\n'
                f'Approximate consumption per circle: {lap_flow if lap_flow is not None else 'NO DATA'}\n'
                f'Approximate lap time: {lap_time if lap_time is not None else 'NO DATA'}\n\n'
                f'Race duration: \n'
                f'{int(race_time.total_seconds() // 3600) if race_time is not None else 'NO DATA'} hours\n'
                f'{round(int(race_time.total_seconds() // 60) - (int(race_time.total_seconds() // 3600) * 60), 3) if race_time is not None else 'NO DATA'} minutes\n\n'
                f'You need to fill up: {round(answer, 3) if answer is not None else 'NO DATA'} liters')


def failed_aprox(lang):
    if lang == 'RUS':
        return 'У нас пока недостаточно данных для примерного расчета топлива на этой трассе'
    else:
        return "We don't have enough data yet to make an approximate calculation."


def fail_tg(lang):
    if lang == 'RUS':
        return f'У нас пока нет трек гайдов для этой трассы под этот автомобиль'
    else:
        return f"We don't have track guide for this car on this track yet"


def fail_setup(lang):
    if lang == 'RUS':
        return 'У нас пока нет сетапов для этой машины и трассы'
    else:
        return "We don't have setups for this car on this track yet"
