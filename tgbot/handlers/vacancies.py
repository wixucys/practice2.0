from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from parser import search_vacancies  # type: ignore
from utils import (
    get_pagination_keyboard,
    get_params,
    prettify_vacancies,
    remove_html_tags_except_b,
)


getvac = Router()


@getvac.message(Command("getvacancies"))
async def get_vacancies(message: Message):
    params = get_params(message.text)
    st = f'<b>{" ".join(params.values()) + f"\n\n"}</b>'
    vacancies = list(await search_vacancies(**params))
    await message.reply(
        remove_html_tags_except_b(st + prettify_vacancies(vacancies)),
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=get_pagination_keyboard(1, 10),
    )


if __name__ == "__main__":
    test1 = "/getvacancies программист, москва, 10000"
    test2 = "/getvacancies программист москва, 10000"
    test3 = "/getvacancies программист москва 10000"
    test4 = "/getvacancies программист москва"
    test5 = "/getvacancies программист, "

    print(1, get_params(test1))
    print(2, get_params(test2))
    print(3, get_params(test3))
    print(4, get_params(test4))
    print(5, get_params(test5))
