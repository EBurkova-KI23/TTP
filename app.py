from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

app = FastAPI()

# Модель пользователя
class User(BaseModel):
    username: str
    email: str

# Имитированная база данных
fake_db: Dict[str, User] = {}

@app.post("/register/")
async def register_user(user: User):
    if user.username in fake_db:
        raise HTTPException(status_code=400, detail="User already exists")
    fake_db[user.username] = user
    return user

@app.get("/user/{username}", response_model=User)
async def get_user(username: str):
    user = fake_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/user/{username}")
async def delete_user(username: str):
    if username not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    del fake_db[username]
    return {"detail": "User deleted"}
