import aiogram
import asyncio
from aiogram import Bot, Dispatcher
from config import API_TOKEN
from handlers.main_root import main_root_router
from handlers.сalculator import calculator_router

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def main(): #роутеры действительно вызываются в порядке, который указан тут
    dp.include_router(main_root_router)  #роутер для основного рута
    dp.include_router(calculator_router) #роутер для калькулятора
    await dp.start_polling(bot)          #запуск диспетчера

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass