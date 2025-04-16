from fastapi import HTTPException

class CustomExceptionA(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=418,
            detail=detail,
            headers={"X-Error": "Custom Error A"}
        )

class CustomExceptionB(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=451,
            detail=detail,
            headers={"X-Error": "Custom Error B"}
        )