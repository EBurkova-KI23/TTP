from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, conint, constr, ValidationError
from fastapi.responses import JSONResponse
from typing import Optional

app = FastAPI()

class User(BaseModel):
    username: str
    age: conint(gt=18)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = 'Unknown'

@app.post("/users/")
def create_user(user: User):
    return user

@app.exception_handler(ValidationError)
async def validation_error_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"message": "Validation error", "details": exc.errors()}
    )

@app.exception_handler(HTTPException)
async def http_error_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": "HTTP error", "details": exc.detail}
    )


# uvicorn 17:app --reload