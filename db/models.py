from db import Base
from sqlalchemy import Column, Integer, String

# vacancy = {
#     "id": id,
#     "name": item["name"],
#     "city": item["area"]["name"],
#     "experience": item["experience"]["name"],
#     "employment": item["employment"]["name"],
#     "requirement": item["snippet"]["requirement"],
#     "responsibility": item["snippet"]["responsibility"],
#     "salary": salary,
#     "link": f"https://hh.ru/vacancy/{id}?from=applicant_recommended&hhtmFrom=main"
# }

class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True)
    hh_id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)
    city = Column(String)
    experience = Column(String)
    employment = Column(String)
    requirement = Column(String)
    responsibility = Column(String)
    salary = Column(Integer)
    link = Column(String)

    def __repr__(self):
        return f"<Vacancy(name={self.name}, city={self.city}, experience={self.experience}, employment={self.employment}, requirement={self.requirement}, responsibility={self.responsibility}, salary={self.salary}, link={self.link})>"