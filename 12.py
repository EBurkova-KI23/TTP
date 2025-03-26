from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

users = {
    "admin": {"password": "adminpass", "role": "admin"},
    "user1": {"password": "userpass", "role": "user"},
    "guest": {"password": "guestpass", "role": "guest"}
}

tokens = {}


class LoginData(BaseModel):
    username: str
    password: str


class UserInfo(BaseModel):
    username: str
    role: str


@app.post("/login")
def login(user_data: LoginData):
    # существование пользователя
    if user_data.username not in users:
        raise HTTPException(status_code=400, detail="Неверный логин")

    # пароль
    if users[user_data.username]["password"] != user_data.password:
        raise HTTPException(status_code=400, detail="Неверный пароль")

    token = f"fake_token_{user_data.username}"
    tokens[token] = users[user_data.username]

    return {"token": token}


def check_role(token: str, required_role: str):
    if token not in tokens:
        raise HTTPException(status_code=401, detail="Неверный токен")

    user_role = tokens[token]["role"]
    if user_role != required_role and user_role != "admin":
        raise HTTPException(status_code=403, detail="Доступ запрещен")


@app.get("/admin-only")
def admin_page(token: str):
    check_role(token, "admin")
    return {"message": "Секретная страница администратора"}


@app.get("/user-page")
def user_page(token: str):
    check_role(token, "user")
    return {"message": "Личный кабинет пользователя"}


@app.get("/public")
def public_page():
    return {"message": "Публичная информация"}


@app.get("/my-info")
def get_my_info(token: str):
    if token not in tokens:
        raise HTTPException(status_code=401, detail="Неверный токен")
    return {
        "username": tokens[token].get("username"),
        "role": tokens[token]["role"]
    }

#  uvicorn 12:app --reload