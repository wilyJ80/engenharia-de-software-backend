from unittest.mock import patch
import pytest

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_acesso_negado():
    response = client.get("/usuarios")

    assert response.status_code == 403

