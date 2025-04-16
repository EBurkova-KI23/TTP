from fastapi import APIRouter
from exceptions import CustomExceptionA, CustomExceptionB
from schemas import ErrorResponse

router = APIRouter()

@router.get("/trigger-a", responses={418: {"model": ErrorResponse}})
async def trigger_error_a(fail: bool = False):
    if fail:
        raise CustomExceptionA("Condition A failed")
    return {"status": "OK"}

@router.get("/trigger-b/{item_id}", responses={451: {"model": ErrorResponse}})
async def trigger_error_b(item_id: int):
    if item_id == 0:
        raise CustomExceptionB("Item not found")
    return {"item_id": item_id}