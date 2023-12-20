import datetime
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor


class User(BaseModel):
    gender: int
    age: int
    city: str

    class Config:
        orm_mode = True


app = FastAPI()

connection = psycopg2.connect(
        database='startml',
        host='postgres.lab.karpov.courses',
        user='robot-startml-ro',
        password='pheiph0hahj1Vaif',
        port=6432,
        cursor_factory=RealDictCursor
    )

@app.get("/")
def root() -> str:
    return 'root'

@app.get('/sum_date')
def sum_date(current_date: datetime.date, offset: int):
    return current_date + datetime.timedelta(days=offset)

@app.post('/user/validate')
def validate(user: User):
    return f'Will add user: {user.name} {user.surname} with age {user.age}'

@app.get('/user/{id}', response_model=User)
def user(id: int):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT gender, age, city FROM "user" WHERE id='%s'""" % id)
        results = cursor.fetchone()

        return User(**results)
