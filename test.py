import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_read_data_success():
    # Имитация успешного ответа внешнего сервиса
    with patch('main.external_service.get_data', new_callable=AsyncMock) as mocked_get:
        mocked_get.return_value = {"id": 1, "name": "Test Data"}

        response = await client.get("/data/1")

        assert response.status_code == 200
        assert response.json() == {"id": 1, "name": "Test Data"}


@pytest.mark.asyncio
async def test_read_data_not_found():
    # Имитация отсутствия данных
    with patch('main.external_service.get_data', new_callable=AsyncMock) as mocked_get:
        mocked_get.side_effect = httpx.HTTPStatusError("Not Found", request=None, response=None)

        response = await client.get("/data/999")

        assert response.status_code == 404
        assert response.json() == {"detail": "Data not found"}


@pytest.mark.asyncio
async def test_create_data_success():
    # Имитация успешного создания данных
    with patch('main.external_service.save_data', new_callable=AsyncMock) as mocked_save:
        mocked_save.return_value = {"id": 2, "name": "New Data"}

        response = await client.post("/data", json={"name": "New Data"})

        assert response.status_code == 200
        assert response.json() == {"id": 2, "name": "New Data"}


@pytest.mark.asyncio
async def test_create_data_failure():
    # Имитация неудачного сохранения данных
    with patch('main.external_service.save_data', new_callable=AsyncMock) as mocked_save:
        mocked_save.side_effect = httpx.HTTPStatusError("Bad Request", request=None, response=None)

        response = await client.post("/data", json={"name": "Bad Request"})

        assert response.status_code == 400
        assert response.json() == {"detail": "Failed to save data"}