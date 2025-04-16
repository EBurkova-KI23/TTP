import pytest
import httpx
from fastapi.testclient import TestClient
from unittest.mock import patch
from XX import app

client = TestClient(app)

# Тестирование чтения пользователя, когда внешний API возвращает данные
@patch('XX.get_external_data')
def test_read_user_success(mock_get_external_data):
    mock_get_external_data.return_value = {"id": 1, "name": "John Doe"}
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John Doe"}

# Тестирование чтения пользователя, когда внешний API возвращает 404
@patch('XX.get_external_data')
def test_read_user_not_found(mock_get_external_data):
    mock_get_external_data.side_effect = httpx.HTTPStatusError("404 Client Error", request=None, response=None)
    response = client.get("/users/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

# Тестирование обновления пользователя
def test_update_user():
    response = client.put("/users/1", json={"name": "Jane Doe"})
    assert response.status_code == 200
    assert response.json() == {"user_id": 1, "updated_data": {"name": "Jane Doe"}}

# Тестирование обновления пользователя с некорректными данными
def test_update_user_invalid_data():
    response = client.put("/users/1", json={"name": ""})  # Проверим, если это вдруг будет запрещено на уровне валидации
    assert response.status_code == 200  # В данном случае проверка успешности будет успешна, так как у нас нет валидации
    assert response.json() == {"user_id": 1, "updated_data": {"name": ""}}

# pytest 20test.py