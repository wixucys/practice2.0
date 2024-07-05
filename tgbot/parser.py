import asyncio
from aiohttp import ClientSession, TCPConnector


# получение id региона по названию города
async def get_region(city: str):
    connector = TCPConnector(ssl=False)
    async with ClientSession(connector=connector) as session:
        areas = await session.get("https://api.hh.ru/areas")
        areas = await areas.json()
        simple_areas = []
        for country in areas:
            if country["name"] == city:
                return country["id"]
            simple_areas.append({"id": country["id"], "name": country["name"]})
            if country.get("areas"):
                for region in country["areas"]:
                    if region["name"] == city:
                        return region["id"]
                    simple_areas.append({"id": region["id"], "name": region["name"]})
                    for city_ in region["areas"]:
                        if city_["name"] == city:
                            return city_["id"]
                        simple_areas.append({"id": city_["id"], "name": city_["name"]})


async def get_vacancies_data(
    query,
    per_page: int = 100,
    city: str | None = None,
    salary: int | None = None,
) -> list[dict]:
    # Отключаем проверку SSL
    connector = TCPConnector(ssl=False)
    url = f"https://api.hh.ru/vacancies?per_page={per_page}&text={query}&only_with_salary=true"
    if salary:
        url += f"&salary={salary}"
    if city:
        if city_id := await get_region(city):
            url += f"&area={city_id}"
    async with ClientSession(connector=connector) as session:
        tasks = [session.get(url + f"&page={page}") for page in range(1, 10)]
        responses = await asyncio.gather(*tasks)
        results = [await response.json() for response in responses]
        all_vacancies = []
        for result in results:
            if items := result.get("items"):
                all_vacancies.extend(items)
        return all_vacancies


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
        "hh_id": int(vacancy["id"]),
        "name": vacancy["name"],
        "city": vacancy["area"]["name"],
        "experience": vacancy["experience"]["name"],
        "employment": vacancy["employment"]["name"],
        "requirement": vacancy["snippet"]["requirement"],
        "responsibility": vacancy["snippet"]["responsibility"],
        "salary": salary_info.split(" ")[1],
        "link": f"https://hh.ru/vacancy/{vacancy['id']}?from=applicant_recommended&hhtmFrom=main",
    }


# Основная асинхронная функция для поиска вакансий
async def search_vacancies(
    query: str,
    city: str | None = None,
    salary: int | None = None,
    per_page: int = 100,
) -> list[dict]:
    vacancies_data = await get_vacancies_data(
        query, city=city, salary=salary, per_page=per_page
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
