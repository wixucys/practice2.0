from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Этот бот позволяет найти вакансии с помощью hh.ru API в выбранном регионе :)"
    )


@router.message(Command("help"))
async def get_help(message: Message):
    await message.answer(
        "Список доступных команд:"
        "\n/start — Начать использование"
        "\n/contacts — Контакты для связи"
        "\n/help — Доступные команды"
        "\n/getvacancies — Получить вакансии в выбранном регионе"
    )


@router.message(Command("contacts"))
async def get_contacts(message: Message):
    await message.answer(
        "Контакты для связи:"
        "\n[Telegram](t.me/penetrat1ve)"
        "\n[GitHub](github.com/wixucys)"
        "\n[Ссылка на сайт HeadHunter](hh.ru)",
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )


@router.message(Command("getvacancies"))
async def get_vacancies(message: Message):
    await message.answer("Введите название региона для поиска доступных вакансий:")


@router.message()
async def echo(message: Message):
    await message.answer(
        "Неизвестная команда. Введите /help или откройте меню для просмотра доступных команд."
    )
