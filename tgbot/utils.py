from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import re


def prettify_vacancy(vacancy) -> str:
    return f"""\
<b>{vacancy["name"]}</b>
<b>Город</b>: {vacancy["city"]}
<b>Опыт</b>: {vacancy["experience"]}
<b>Занятость</b>: {vacancy["employment"]}
<b>Требования</b>: {vacancy["requirements"]}
<b>Обязанности</b>: {vacancy["responsibilities"]}
<b>Зарплата</b>: {vacancy["salary"]}
<b>Ссылка</b>: {vacancy["link"]}
"""


def get_pagination_keyboard(
    current_page: int, total_pages: int
) -> InlineKeyboardMarkup:

    buttons = []
    if current_page > 1:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=f"page_{current_page}_{current_page - 1}",
                )
            ]
        )
    if current_page < total_pages:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="Вперёд ➡️",
                    callback_data=f"page_{current_page}_{current_page + 1}",
                )
            ]
        )
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def prettify_vacancies(vacancies) -> str:
    return "\n\n".join(prettify_vacancy(vacancy) for vacancy in vacancies)


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
    pre_list = [str(item).capitalize() for item in pre_list]
    params = zip(params_list, pre_list)
    return dict(params)

def get_text_params(text: str) -> dict:
    text = text.strip()
    text = text.split()
    params = ["query", "city", "salary"][:len(text)]
    text = [str(item).capitalize() for item in text]
    params = zip(params, text)
    return dict(params)


def remove_html_tags_except_b(text: str) -> str:
    # Удаляем все теги, кроме <b> и </b>
    clean_text = re.sub(r"<(?!\/?b\b)[^>]*>", "", text)
    return clean_text
