from aiogram import Router
from aiogram.types import CallbackQuery
from utils import (
    get_text_params,
    prettify_vacancies,
    get_pagination_keyboard,
    remove_html_tags_except_b,
)
from parser import search_vacancies  # type: ignore

cr = Router()


@cr.callback_query()
async def page_callback_handler(call: CallbackQuery):
    if call.data.startswith("page_"):
        # Извлекаем номер страницы из callback_data
        before_page_number = int(call.data.split("_")[1])
        current_page_number = int(call.data.split("_")[2])
        # await call.message.answer(f"Страница {page_number}")
        text = call.message.text.split("\n\n")[0]
        print(text)
        # Здесь должен быть ваш код для получения данных о вакансиях на запрошенной странице
        # Например, vacancies = await search_vacancies(page=page_number)
        # Для примера просто отправим номер страницы
        params = get_text_params(text)
        print(params)
        vacancies = list(await search_vacancies(**params, page=current_page_number))
        prettify__vacancies = prettify_vacancies(vacancies)
        await call.message.edit_text(
            remove_html_tags_except_b(f"<b>{text}</b>\n\n" + f"{prettify__vacancies}"),
            reply_markup=get_pagination_keyboard(current_page_number, 10),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )  # Предположим, что всего 5 страниц
