import pytest

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_get_example():
    response = client.get("/example/")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Exemplo"
