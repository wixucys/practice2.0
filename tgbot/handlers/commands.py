from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Этот бот позволяет найти вакансии с сайта hh.ru :)"
        "\n\nВведите /help для поиска доступных команд."
        "\n\nДля поиска доступных вакансий введите запрос в формате:"
        "\n/getvacancies программист Москва 100000"
    )


@router.message(Command("help"))
async def get_help(message: Message):
    await message.answer(
        "Список доступных команд:"
        "\n/start — Начать использование"
        "\n/contacts — Контакты для связи"
        "\n/help — Помощь"
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
