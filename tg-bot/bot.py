import asyncio
import logging
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers.handlers import router


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # логирование помогает видеть действия бота
    # чтобы при выключении бота не выводилась ошибка, пишем конструкцию
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
