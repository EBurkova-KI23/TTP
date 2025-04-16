from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from typing import List
from pydantic import BaseModel
from datetime import datetime, timedelta

# Компоненты для JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Модели данных
class User(BaseModel):
    username: str
    role: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    role: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Хранилище пользователей
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Administrator User",
        "email": "admin@example.com",
        "hashed_password": "fakehashedpasswordadmin",
        "role": "admin",
    },
    "user": {
        "username": "user",
        "full_name": "Regular User",
        "email": "user@example.com",
        "hashed_password": "fakehashedpassworduser",
        "role": "user",
    },
    "guest": {
        "username": "guest",
        "full_name": "Guest User",
        "email": "guest@example.com",
        "hashed_password": "fakehashedpasswordguest",
        "role": "guest",
    },
}

# Функции для JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Аутентификация пользователя
async def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# Авторизация на основе роли
def role_required(required_role: str):
    def role_checker(current_user: TokenData = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return current_user
    return role_checker

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception
    user = await get_user(fake_users_db, token_data.username)
    if user is None:
        raise credentials_exception
    return token_data

app = FastAPI()

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(fake_users_db, form_data.username)
    if not user or user.hashed_password != form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected_resource")
async def read_protected_resource(current_user: TokenData = Depends(get_current_user)):
    return {"msg": "This is a protected resource", "user": current_user.username}

@app.get("/admin")
async def read_admin_data(current_user: TokenData = Depends(role_required("admin"))):
    return {"msg": "Admin data", "user": current_user.username}

@app.get("/user")
async def read_user_data(current_user: TokenData = Depends(role_required("user"))):
    return {"msg": "User data", "user": current_user.username}

@app.get("/guest")
async def read_guest_data(current_user: TokenData = Depends(role_required("guest"))):
    return {"msg": "Guest data", "user": current_user.username}

# Запуск сервера
# uvicorn main:app --reload