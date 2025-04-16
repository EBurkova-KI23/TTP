from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from fastapi.exceptions import RequestValidationError

app = FastAPI()

class ErrorResponseModel(BaseModel):
    status_code: int
    message: str
    error_code: int
    error_handle_time: Optional[str] = None

class UserNotFoundException(Exception):
    pass

class InvalidUserDataException(Exception):
    pass

@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return JSONResponse(
        status_code=404,
        content=ErrorResponseModel(
            status_code=404,
            message="User not found",
            error_code=1001,
            error_handle_time=error_time
        ).dict(),
        headers={"X-ErrorHandleTime": error_time}
    )

@app.exception_handler(InvalidUserDataException)
async def invalid_user_data_exception_handler(request: Request, exc: InvalidUserDataException):
    error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return JSONResponse(
        status_code=400,
        content=ErrorResponseModel(
            status_code=400,
            message="Invalid user data",
            error_code=1002,
            error_handle_time=error_time
        ).dict(),
        headers={"X-ErrorHandleTime": error_time}
    )

class User(BaseModel):
    username: str
    email: str

@app.post("/register/")
async def register_user(user: User):
    try:
        if user.username == "test":
            raise UserNotFoundException()
        if "@" not in user.email:
            raise InvalidUserDataException()
        return user
    except Exception as e:
        error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return JSONResponse(
            status_code=500,
            content=ErrorResponseModel(
                status_code=500,
                message=f"Internal Server Error: {str(e)}",
                error_code=1003,
                error_handle_time=error_time
            ).dict(),
            headers={"X-ErrorHandleTime": error_time}
        )

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    try:
        if user_id == 0:
            raise UserNotFoundException()
        return {"user_id": user_id}
    except Exception as e:
        error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return JSONResponse(
            status_code=500,
            content=ErrorResponseModel(
                status_code=500,
                message=f"Internal Server Error: {str(e)}",
                error_code=1003,
                error_handle_time=error_time
            ).dict(),
            headers={"X-ErrorHandleTime": error_time}
        )

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"message": "Validation error", "details": exc.errors()}
    )

@app.exception_handler(HTTPException)
async def http_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


# uvicorn 181:app --reload