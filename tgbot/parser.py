import asyncio
from aiohttp import ClientSession, TCPConnector


# получение id региона по названию города
async def get_region(city: str):
    connector = TCPConnector(ssl=False)
    async with ClientSession(connector=connector) as session:
        regions = await session.get("https://api.hh.ru/areas")
        regions = await regions.json()
        city_id = [region["id"] for region in regions if region["name"] == city]
        return city_id[0] if city_id else None


async def get_vacancies_data(
    query,
    page: int = 1,
    per_page: int = 2,
    city: str | None = None,
    salary: int | None = None,
) -> dict:
    # Отключаем проверку SSL
    connector = TCPConnector(ssl=False)
    url = f"https://api.hh.ru/vacancies?per_page={per_page}&text={query}&only_with_salary=true"
    if salary:
        url += f"&salary={salary}"
    if city:
        if city_id := await get_region(city):
            url += f"&area={city_id}"
    async with ClientSession(connector=connector) as session:
        response = await session.get(url + f"&page={page}")
        result = await response.json()
        return result["items"]


# Обработка данных о вакансии
def process_vacancy_data(vacancy):
    salary = vacancy.get("salary")
    if salary is None:
        salary_info = "не указана"
    else:
        salary_from = salary.get("from", "")
        salary_to = salary.get("to", "")
        salary_info = (
            f"от {salary_from}"
            if salary_from
            else f"до {salary_to}" if salary_to else "не указана"
        )

    return {
        "id": vacancy["id"],
        "name": vacancy["name"],
        "city": vacancy["area"]["name"],
        "experience": vacancy["experience"]["name"],
        "employment": vacancy["employment"]["name"],
        "requirements": vacancy["snippet"]["requirement"],
        "responsibilities": vacancy["snippet"]["responsibility"],
        "salary": salary_info,
        "link": f"https://hh.ru/vacancy/{vacancy['id']}?from=applicant_recommended&hhtmFrom=main",
    }


# Основная асинхронная функция для поиска вакансий
async def search_vacancies(
    query: str,
    city: str | None = None,
    salary: int | None = None,
    page: int = 1,
    per_page: int = 2,
) -> list[dict]:
    vacancies_data = await get_vacancies_data(
        query, city=city, salary=salary, page=page, per_page=per_page
    )
    processed_vacancies = []
    for data in vacancies_data:
        processed_vacancies.append(process_vacancy_data(data))
    return processed_vacancies


# Точка входа в программу
if __name__ == "__main__":
    query = "Python"
    city = "Москва"
    salary = 100000
    vacancies = asyncio.run(search_vacancies(query, city=city, salary=salary))
    print(vacancies)
