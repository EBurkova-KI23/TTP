from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Определение своих пользовательских исключений
class CustomExceptionA(HTTPException):
    def __init__(self, detail: str = "A specific error occurred", headers: dict = None):
        super().__init__(status_code=418, detail=detail, headers=headers)

class CustomExceptionB(HTTPException):
    def __init__(self, detail: str = "B specific error occurred", headers: dict = None):
        super().__init__(status_code=451, detail=detail, headers=headers)

# Модель для представления ошибки
class ErrorResponse(BaseModel):
    error_type: str
    message: str
    error_code: int
    details: str

# Обработчики исключений
def custom_exception_a_handler(request, exc: CustomExceptionA):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_type": "CustomErrorA",
            "message": "Custom Error A Occurred",
            "error_code": 1001,
            "details": exc.detail
        },
        headers=exc.headers
    )

def custom_exception_b_handler(request, exc: CustomExceptionB):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_type": "CustomErrorB",
            "message": "Custom Error B Occurred",
            "error_code": 1002,
            "details": exc.detail
        },
        headers=exc.headers
    )

# Создание FastAPI приложения
app = FastAPI()

# Регистрация обработчиков исключений
app.add_exception_handler(CustomExceptionA, custom_exception_a_handler)
app.add_exception_handler(CustomExceptionB, custom_exception_b_handler)

# Создание роутера
router = APIRouter()

# Эндпоинты для генерации исключений
@router.get("/trigger-a")
def trigger_a():
    raise CustomExceptionA(detail="This is a custom exception A message")

@router.get("/trigger-b")
def trigger_b():
    raise CustomExceptionB(detail="This is a custom exception B message")

# Подключение роутера к приложению
app.include_router(router)


# uvicorn 16:app --reload