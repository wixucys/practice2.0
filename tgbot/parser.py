import asyncio
from aiohttp import ClientSession, TCPConnector


async def get_vacancies_data(query, pages=20):
    # Отключаем проверку SSL
    connector = TCPConnector(ssl=False)
    async with ClientSession(connector=connector) as session:
        base_url = "https://api.hh.ru/vacancies"
        tasks = [
            session.get(f"{base_url}?page={page}&per_page=100&text={query}")
            for page in range(pages)
        ]
        responses = await asyncio.gather(*tasks)
        results = [await response.json() for response in responses]
        return results


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
async def search_vacancies_async(query):
    vacancies_data = await get_vacancies_data(query)
    processed_vacancies = []
    for data in vacancies_data:
        for item in data.get("items", []):
            processed_vacancies.append(process_vacancy_data(item))
    return processed_vacancies


# Точка входа в программу
if __name__ == "__main__":
    query = "Python"
    vacancies = asyncio.run(search_vacancies_async(query))
    print(vacancies)
