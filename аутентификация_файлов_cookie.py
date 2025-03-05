from fastapi import FastAPI, HTTPException, Request, Response, Form
from fastapi.responses import JSONResponse

app = FastAPI()

# Хранилище пользовательских данных
fake_users_db = {
    "user123": {
        "username": "user123",
        "password": "password123",
        "profile": {"name": "John Doe", "email": "john@example.com"}
    }
}

# Хранилище сессий
session_tokens = {}

@app.post("/login")
def login(response: Response, username: str = Form(...), password: str = Form(...)):
    user = fake_users_db.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Уникальное значение для session_token генерируем с помощью UUID
    import uuid
    session_token = str(uuid.uuid4())
    # Сохраняем токен в памяти
    session_tokens[session_token] = user
    # Устанавливаем cookie
    response.set_cookie(key="session_token", value=session_token, httponly=True)
    return {"message": "Login successful"}


@app.get("/user")
def read_user(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token or session_token not in session_tokens:
        return JSONResponse(content={"message": "Unauthorized"}, status_code=401)

    user = session_tokens[session_token]
    return {"profile": user["profile"]}


# uvicorn аутентификация_файлов_cookie:app --reload
