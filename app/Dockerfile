#контейнер, который будет взят за основу
FROM python:3.13.0-slim

LABEL authors="rozzenrose"

# установим параметры окружения
ENV HOME=/home/'ACC_helper' \
    APP_HOME=/home/'ACC_helper'/app \
    PYTHONPATH="$PYTHONPATH:/home/'ACC_helper'" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DB_HOST=ACC_helper_db \
    DB_PORT=5432 \
    DB_USER=postgres \
    DB_PASS=2580 \
    DB_NAME=postgres

# создадим домашнюю директорию для пользователя(/home/helper)
# и директорию для проекта(/home/helper/app)
RUN mkdir -p $APP_HOME \
 && groupadd -r helper \
 && useradd -r -g helper helper

# устанавливаем рабочую директорию
WORKDIR $HOME

# копирование проекта ACC_helper в рабочую директорию
COPY app app
ADD alembic.ini .

# обновление pip
# установка зависимостей из списка requirements.txt
# изменение владельца, для всех директорий и файлов проекта, на пользователя helper
RUN pip install --upgrade pip \
 && pip install -r app/requirements.txt \
 && chown -R helper:helper .

# изменение рабочего пользователя на helper \
USER helper