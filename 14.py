from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import asyncio

app = FastAPI()

todos = []

class Todo(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    completed: bool = False

#имитация асинхронной операции
async def async_operation():
    await asyncio.sleep(0.1)  #небольшая задержка

# новый Todo
@app.post("/todos", response_model=Todo)
async def create_todo(todo: Todo):
    await async_operation()
    todo.id = len(todos) + 1
    todos.append(todo)
    return todo

@app.get("/todos/{todo_id}", response_model=Todo)
async def read_todo(todo_id: int):
    await async_operation()
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, updated_todo: Todo):
    await async_operation()
    for todo in todos:
        if todo.id == todo_id:
            todo.title = updated_todo.title
            todo.description = updated_todo.description
            todo.completed = updated_todo.completed
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    await async_operation()
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")

@app.get("/todos", response_model=List[Todo])
async def read_all_todos():
    await async_operation()
    return todos

#  uvicorn 14:app --reload