from fastapi import FastAPI
from pydantic import BaseModel
from typing import List


# Определяем Pydantic модель для входных данных
class Feedback(BaseModel):
    name: str
    message: str


# Создаем экземпляр FastAPI
app = FastAPI()

# Хранилище для отзывов
feedback_storage: List[Feedback] = []


# Маршрут для приема отзывов
@app.post("/feedback")
async def receive_feedback(feedback: Feedback):
    # Сохраняем отзыв в хранилище
    feedback_storage.append(feedback)

    # Формируем сообщение об успешном завершении
    response_message = {
        "message": f"Feedback received. Thank you, {feedback.name}!"
    }

    return response_message

# uvicorn 5:app --reload