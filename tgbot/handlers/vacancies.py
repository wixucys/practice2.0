from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


getvac = Router()


def get_params(text: str) -> dict:
    text = text.strip()
    if text.endswith(","):
        text = text[:-1]
    pre_list = text.split(",")
    pre_list = [var.strip() for var in pre_list]
    for var in pre_list:
        if " " not in var:
            continue
        else:
            pre_list.remove(var)
            pre_list = var.split()[1:] + pre_list
    len_list = len(pre_list)

    params_list = ["query", "city", "salary"][:len_list]
    params = zip(params_list, pre_list)
    return dict(params)


@getvac.message(Command("getvacancies"))
async def get_vacancies(message: Message):
    params = get_params(message.text)
    await message.answer(f"Вы ввели:\n\n{params}")
