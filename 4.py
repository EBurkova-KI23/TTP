from fastapi import FastAPI
from pydantic import BaseModel

# Определяем нашу модель Pydantic
class User(BaseModel):
    name: str
    age: int

# Создаем приложение FastAPI
app = FastAPI()

# Определяем маршрут /user, который принимает POST-запросы
@app.post("/user")
async def create_user(user: User):
    # Проверяем, является ли пользователь взрослым
    is_adult = user.age >= 18
    # Формируем ответ с дополнительным полем is_adult
    response = user.dict()
    response.update({"is_adult": is_adult})
    return response

# uvicorn 4:app --reload