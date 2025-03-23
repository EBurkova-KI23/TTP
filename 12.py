from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict

app = FastAPI()

# Заглушка для пользователей и их ролей
fake_users_db = {
    "admin@example.com": {"role": "admin"},
    "user@example.com": {"role": "user"},
    "guest@example.com": {"role": "guest"},
}

# Определим роли и их разрешения
permissions = {
    "admin": ["create", "read", "update", "delete"],
    "user": ["read", "update"],
    "guest": ["read"],
}

security = HTTPBearer()


# Функция проверки пользователя и его роли
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Здесь предположим, что аутентификация JWT уже выполнена и возвращает email
    user_email = credentials.credentials  # В реальных условиях, например, декодируйте JWT токен, чтобы получить пользователя
    user = fake_users_db.get(user_email)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")

    return user


# Декоратор для проверки ролей
def role_required(required_role: str):
    def role_wrapper(current_user: Dict = Depends(get_current_user)):
        if current_user['role'] != required_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
        return current_user

    return role_wrapper


@app.post("/resource")
def create_resource(user: Dict = Depends(role_required("admin"))):
    return {"message": "Resource created"}


@app.get("/resource")
def read_resource(user: Dict = Depends(role_required("guest"))):
    return {"message": "Resource data"}


@app.put("/resource")
def update_resource(user: Dict = Depends(role_required("user"))):
    return {"message": "Resource updated"}


@app.get("/protected_resource")
def protected_resource(user: Dict = Depends(role_required("user"))):
    return {"message": "Access granted to protected resource"}


@app.get("/admin_resource")
def admin_resource(user: Dict = Depends(role_required("admin"))):
    return {"message": "Access granted to admin resource"}

# Тестирование различных ролей
# 1. admin@example.com: доступ к /resource (POST), /protected_resource (GET), /admin_resource (GET)
# 2. user@example.com: доступ к /resource (GET), /protected_resource (GET), /resource (PUT)
# 3. guest@example.com: доступ только к /resource (GET)

# Если тестировать с curl или Postman, то нужно будет использовать JWT токены.
# curl -H "Authorization: Bearer admin@example.com" http://localhost:8000/resource

# uvicorn 12:app --reload
