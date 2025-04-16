import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_register_user():
    response = client.post("/register/", json={"username": "testuser", "email": "test@example.com"})
    assert response.status_code == 200
    assert response.json() == {"username": "testuser", "email": "test@example.com"}

    # Тест на регистрацию существующего пользователя
    response = client.post("/register/", json={"username": "testuser", "email": "test@example.com"})
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}

def test_get_user():
    response = client.post("/register/", json={"username": "testuser2", "email": "test2@example.com"})
    assert response.status_code == 200
    assert response.json() == {"username": "testuser2", "email": "test2@example.com"}

    response = client.get("/user/testuser2")
    assert response.status_code == 200
    assert response.json() == {"username": "testuser2", "email": "test2@example.com"}

    # Тест на получение несуществующего пользователя
    response = client.get("/user/nonexistentuser")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_delete_user():
    response = client.post("/register/", json={"username": "testuser3", "email": "test3@example.com"})
    assert response.status_code == 200

    response = client.delete("/user/testuser3")
    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted"}

    # Тест на удаление несуществующего пользователя
    response = client.delete("/user/nonexistentuser")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

# pytest 19.py