from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

class UserCreate(BaseModel):
    name: str = Field(..., description="Имя пользователя")
    email: EmailStr = Field(..., description="Адрес электронной почты пользователя")
    age: int = Field(default=None, gt=0, description="Возраст пользователя (должен быть положительным числом)")
    is_subscribed: bool = Field(default=None, description="Флажок, указывающий, подписан ли пользователь на новостную рассылку")

@app.post("/create_user")
async def create_user(user: UserCreate):
    return user

# uvicorn Обработка_HTTP-запросов:app --reload