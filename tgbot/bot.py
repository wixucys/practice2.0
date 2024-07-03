import asyncio
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers.handlers import router

load_dotenv()
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
TOKEN = os.getenv("TOKEN")


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    # чтобы при выключении бота не выводилась ошибка, пишем конструкцию
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
