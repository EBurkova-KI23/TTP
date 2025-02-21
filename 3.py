from fastapi import FastAPI
from models import User

app = FastAPI()

# Создаем экземпляр модели User
user_instance = User(name="John Doe", id=1)

# Определяем маршрут для получения данных о пользователе
@app.get("/users", response_model=User)
def get_user():
    return user_instance

# Стартовое сообщение для проверки
@app.get("/")
def read_root():
    return {"Hello": "World"}

# uvicorn 3:app --reload