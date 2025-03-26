from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
import random

# Конфигурация приложения
SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Определяем модель данных для входа
class LoginData(BaseModel):
    username: str
    password: str

# Функция аутентификации пользователя
def authenticate_user(username: str, password: str) -> bool:
    return random.choice([True, False])

# Генерируем токен JWT
def create_jwt_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Конечная точка для входа и получения токена
@app.post("/login")
def login(login_data: LoginData):
    if not authenticate_user(login_data.username, login_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_jwt_token(
        data={"sub": login_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token}

# Создаем зависимость, которая будет использоваться для аутентификации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Проверяем токен и возвращаем пользователя
def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    return username

# Защищенная конечная точка
@app.get("/protected_resource")
def read_protected(username: str = Depends(verify_token)):
    return {"message": f"Hello, {username}. You have accessed protected data."}

# uvicorn аутентификацияJWT:app --reload
