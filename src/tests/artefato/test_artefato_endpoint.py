from unittest.mock import AsyncMock, patch
import uuid
from datetime import datetime
import os
import sys

# Adiciona o diretório src ao sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

# Mock das conexões de banco antes de importar a aplicação
with patch('db.connection.Connection'):
    from fastapi.testclient import TestClient
    from main import app

client = TestClient(app)

def artefatos_fake(quant: int):
    lista = []
    for i in range(quant):
        lista.append({
            "id": str(uuid.uuid4()),
            "nome": f"Artefato {i}",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
    return lista

@patch("routes.artefatos_router.get_db", new_callable=AsyncMock)
@patch("service.artefato_service.create_artefato", new_callable=AsyncMock)
def test_create_artefato(mock_create, mock_db):
    artefato = artefatos_fake(1)[0]
    mock_db.return_value = "fake_db"
    mock_create.return_value = artefato

    response = client.post("/artefatos/", json={
        "nome": artefato["nome"]
    })

    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == artefato["nome"]