from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import select, or_
from db.db import async_session_maker
from db.models import Vacancy
import re


# {
#         "hh_id": int(vacancy["id"]),
#         "name": vacancy["name"],
#         "city": vacancy["area"]["name"],
#         "experience": vacancy["experience"]["name"],
#         "employment": vacancy["employment"]["name"],
#         "requirement": vacancy["snippet"]["requirement"],
#         "responsibility": vacancy["snippet"]["responsibility"],
#         "salary": salary_info.split(' ')[1],
#         "link": f"https://hh.ru/vacancy/{vacancy['id']}?from=applicant_recommended&hhtmFrom=main",
#     }


def prettify_vacancy(vacancy: Vacancy) -> str:
    return f"""\
<b>{vacancy.name}</b>
<b>Город</b>: {vacancy.city}
<b>Опыт</b>: {vacancy.experience}
<b>Занятость</b>: {vacancy.employment}
<b>Требования</b>: {vacancy.requirement}
<b>Обязанности</b>: {vacancy.responsibility}
<b>Зарплата</b>: {vacancy.salary}
<b>Ссылка</b>: {vacancy.link}
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


# def get_params(text: str) -> dict:


def get_params(text: str) -> dict:
    text = text.lstrip("/getvacancies").strip()
    text = text.split(f'\n')
    pre_list = [item.strip().strip(',') for item in text]
    params_list = ["query", "city", "salary"][:len(pre_list)]
    pre_list = [str(item).capitalize() for item in pre_list]
    params = zip(params_list, pre_list)
    return dict(params)


def get_text_params(text: str) -> dict:
    text = text.strip()
    text = text.split()
    params = ["query", "city", "salary"][: len(text)]
    text = [str(item).capitalize() for item in text]
    params = zip(params, text)
    return dict(params)


def remove_html_tags_except_b(text: str) -> str:
    # Удаляем все теги, кроме <b> и </b>
    clean_text = re.sub(r"<(?!\/?b\b)[^>]*>", "", text)
    return clean_text


# vacancy = {
#         "id": vacancy["id"],
#         "name": vacancy["name"],
#         "city": vacancy["area"]["name"],
#         "experience": vacancy["experience"]["name"],
#         "employment": vacancy["employment"]["name"],
#         "requirements": vacancy["snippet"]["requirement"],
#         "responsibilities": vacancy["snippet"]["responsibility"],
#         "salary": salary_info,
#         "link": f"https://hh.ru/vacancy/{vacancy['id']}?from=applicant_recommended&hhtmFrom=main",
#     }


async def get_vacancies_from_db(
    query: str,
    city: str | None = None,
    salary: int | None = None,
    page: int | None = None,
    page_size: int | None = 2,
) -> list[Vacancy]:
    async with async_session_maker() as session:
        async with session.begin():
            query = (
                select(Vacancy)
                .filter(
                    or_(
                        Vacancy.name.like(f"%{query}%"),
                        Vacancy.requirement.like(f"%{query}%"),
                    ),
                    Vacancy.city == city,
                    Vacancy.salary.like(f"%{salary}%"),
                )
                .limit(page_size)
                .offset((page - 1) * page_size)
            )
            vacancies = await session.execute(query)
            vacancies = vacancies.scalars().all()
            return vacancies


async def add_vacancies(
    vacancies: list,
) -> None:
    async with async_session_maker() as db:
        async with db.begin():
            vacancy_instances = [Vacancy(**vacancy) for vacancy in vacancies]
            # получаем все hh_id из базы
            existing_vacancy_hh_ids = [
                row[0]
                for row in await db.execute(select(Vacancy.hh_id))
                if row[0] is not None
            ]
            # фильтруем вакансии по hh_id
            vacancy_instances = [
                vacancy
                for vacancy in vacancy_instances
                if vacancy.hh_id not in existing_vacancy_hh_ids
            ]
            db.add_all(vacancy_instances)
        await db.commit()


async def get_max_pages_count(
    query: str,
    city: str | None = None,
    salary: int | None = None,
    page_size: int | None = 2,
) -> int:
    async with async_session_maker() as session:
        async with session.begin():
            query = select(Vacancy).filter(
                or_(
                    Vacancy.name.like(f"%{query}%"),
                    Vacancy.requirement.like(f"%{query}%"),
                ),
                Vacancy.city == city,
                Vacancy.salary.like(f"%{salary}%"),
            )
            count = await session.execute(query)
            count = count.scalars().all()
            count = len(count)
            return count // page_size + 1 if count % page_size else count // page_size
