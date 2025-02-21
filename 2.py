from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class NumberInput(BaseModel):
    num1: float
    num2: float

@app.post("/calculate")
async def calculate(numbers: NumberInput):
    result = numbers.num1 + numbers.num2
    return {"result": result}

# uvicorn 2:app --reload