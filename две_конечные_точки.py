from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List

app = FastAPI()

# Пример
sample_products = [
    {
        "product_id": 123,
        "name": "Smartphone",
        "category": "Electronics",
        "price": 599.99
    },
    {
        "product_id": 456,
        "name": "Phone Case",
        "category": "Accessories",
        "price": 19.99
    },
    {
        "product_id": 789,
        "name": "Iphone",
        "category": "Electronics",
        "price": 1299.99
    },
    {
        "product_id": 101,
        "name": "Headphones",
        "category": "Accessories",
        "price": 99.99
    },
    {
        "product_id": 202,
        "name": "Smartwatch",
        "category": "Electronics",
        "price": 299.99
    }
]

@app.get("/product/{product_id}")
def get_product(product_id: int):
    for product in sample_products:
        if product["product_id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/products/search", response_model=List[dict])
def search_products(
    keyword: str,
    category: Optional[str] = None,
    limit: int = 10
):
    results = []
    for product in sample_products:
        if keyword.lower() in product["name"].lower():
            if category:
                if product["category"].lower() == category.lower():
                    results.append(product)
            else:
                results.append(product)
    return results[:limit]

@app.get("/")
def read_root():
    return {"Hello": "World"}

# uvicorn две_конечные_точки:app --reload