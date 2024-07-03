from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

getvac = Router()


@getvac.message(Command("getvacancies"))
async def get_vacancies(message: Message):
    await message.answer("Введите название региона для поиска доступных вакансий:")
