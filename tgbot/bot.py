import asyncio
from aiogram import Bot, Dispatcher
from handlers.callback import cr
from handlers.commands import router
from handlers.vacancies import getvac
from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(cr)
dp.include_router(router)
dp.include_router(getvac)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    # чтобы при выключении бота не выводилась ошибка, пишем конструкцию
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
