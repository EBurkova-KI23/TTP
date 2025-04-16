from pydantic import BaseModel

class ErrorResponse(BaseModel):
    error_type: str
    message: str
    error_code: int
    details: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "error_type": "CustomErrorA",
                "message": "Something went wrong",
                "error_code": 1001,
                "details": "Additional error information"
            }
        }