from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta
import random

# Создаем приложение FastAPI
app = FastAPI()

# Конфигурации для JWT
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Функция проверки учётных данных пользователя
def authenticate_user(username: str, password: str) -> bool:
    # Здесь должна быть реализация проверки данных пользователя.
    # Используем заглушку.
    return random.choice([True, False])


# Функция генерации JWT токена
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Конечная точка для логина
@app.post("/login")
async def login(user_name: str, password: str):
    if not authenticate_user(user_name, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token}


# Мидлваре для проверки JWT токена
security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token is invalid")


# Защищенная конечная точка
@app.get("/protected_resource")
async def protected_resource(token: dict = Depends(verify_token)):
    return {"message": "Access granted to protected resource", "user": token["sub"]}

