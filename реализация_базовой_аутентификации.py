from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED
from typing import Optional
from fastapi.responses import JSONResponse

app = FastAPI()

security = HTTPBasic()

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)) -> Optional[str]:
    correct_username = "user123"
    correct_password = "securepassword"

    if credentials.username == correct_username and credentials.password == correct_password:
        return "You got my secret, welcome"
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get("/login")
async def login(message: str = Depends(verify_credentials)) -> JSONResponse:
    return JSONResponse(content={"message": message})

#uvicorn 12:app --reload

# uvicorn реализация_базовой_аутентификации:app --reload