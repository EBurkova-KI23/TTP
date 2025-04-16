from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

# Внешняя функция для получения данных из внешнего API
async def get_external_data(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
        response.raise_for_status()
        return response.json()

# Конечная точка для получения данных пользователя
@app.get("/users/{user_id}")
async def read_user(user_id: int):
    try:
        user_data = await get_external_data(user_id)
        return user_data
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=404, detail="User not found")

# Конечная точка для обновления пользователя (имитация)
@app.put("/users/{user_id}")
async def update_user(user_id: int, user_data: dict):
    return {"user_id": user_id, "updated_data": user_data}