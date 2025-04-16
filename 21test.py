import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from XXI import app, get_db
from models import Base

# URL для тестовой базы данных
TEST_DATABASE_URL = "postgresql://postgres:123456@localhost:5432/my_db_test"
test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

def test_create_user():
    response = client.post("/users/", json={"username": "testuser", "email": "testuser@example.com"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_get_user():
    response = client.post("/users/", json={"username": "testuser2", "email": "testuser2@example.com"})
    user_id = response.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser2"

def test_update_user():
    response = client.post("/users/", json={"username": "testuser3", "email": "testuser3@example.com"})
    user_id = response.json()["id"]
    response = client.put(f"/users/{user_id}", json={"username": "updateduser", "email": "updateduser@example.com"})
    assert response.status_code == 200
    assert response.json()["username"] == "updateduser"

#pytest 21test.py