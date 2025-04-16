from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Product

# Настройка подключения к базе данных
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:123456@localhost:5432/alembic"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание таблиц в базе данных (если они не созданы)
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Модель для добавления продукта
class ProductCreate(BaseModel):
    title: str
    price: float
    count: int
    description: str


# Модель для обновления продукта
class ProductUpdate(BaseModel):
    title: str | None
    price: float | None
    count: int | None
    description: str | None


# Пример API-эндпоинта для работы с продуктами
@app.get("/products/")
def read_products():
    db = SessionLocal()
    products = db.query(Product).all()
    return [{"id": product.id, "title": product.title, "price": product.price, "count": product.count,
             "description": product.description} for product in products]


# Пример API-эндпоинта для добавления нового продукта
@app.post("/products/")
def create_product(product: ProductCreate):
    try:
        db = SessionLocal()
        print("Добавление продукта...")
        new_product = Product(title=product.title, price=product.price, count=product.count,
                              description=product.description)
        db.add(new_product)
        print("Продукт добавлен в сессию.")
        db.commit()
        print("Транзакция коммитится.")
        db.refresh(new_product)
        print("Продукт добавлен в базу данных.")
        return {"id": new_product.id, "title": new_product.title, "price": new_product.price,
                "count": new_product.count, "description": new_product.description}
    except Exception as e:
        db.rollback()
        print(f"Ошибка: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Пример API-эндпоинта для обновления продукта
@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate):
    try:
        db = SessionLocal()
        existing_product = db.query(Product).filter(Product.id == product_id).first()
        if existing_product is None:
            raise HTTPException(status_code=404, detail="Product not found")

        if product.title:
            existing_product.title = product.title
        if product.price:
            existing_product.price = product.price
        if product.count:
            existing_product.count = product.count
        if product.description:
            existing_product.description = product.description

        db.commit()
        db.refresh(existing_product)
        return {"id": existing_product.id, "title": existing_product.title, "price": existing_product.price,
                "count": existing_product.count, "description": existing_product.description}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# Пример API-эндпоинта для удаления продукта
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    try:
        db = SessionLocal()
        product = db.query(Product).filter(Product.id == product_id).first()
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        db.delete(product)
        db.commit()
        return {"message": f"Product with ID {product_id} deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# uvicorn main:app --reload
"""
{
    "title": "bread",
    "price": 50,
    "count": 20,
    "description": "Sample"
}

{
   "title": "milk",
   "price": "100",
   "count": "25",
   "description": "pupupu"
}
"""