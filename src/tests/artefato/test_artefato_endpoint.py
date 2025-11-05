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



@patch("routes.artefatos_router.get_db", new_callable=AsyncMock)
@patch("service.artefato_service.get_all_artefatos", new_callable=AsyncMock)
def test_get_all_artefatos(mock_get_all, mock_db):  
    artefatos = artefatos_fake(5)
    mock_db.return_value = "fake_db"
    mock_get_all.return_value = artefatos
    artefatos_response = []
    for i in artefatos:
        artefatos_response.append({
            "id": i["id"],
            "nome": i["nome"],
        })
    

    response = client.get("/artefatos/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == artefatos_response.__len__()
    assert data == artefatos_response


@patch("routes.artefatos_router.get_db", new_callable=AsyncMock)
@patch("service.artefato_service.get_artefato_by_id", new_callable=AsyncMock)
def test_get_artefato_by_id(mock_get_one, mock_db): 
    artefato = artefatos_fake(1)[0]
    mock_db.return_value = "fake_db"
    mock_get_one.return_value = artefato

    response = client.get(f"/artefatos/{artefato['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == artefato["id"]
    assert data["nome"] == artefato["nome"]


@patch("routes.artefatos_router.get_db", new_callable=AsyncMock)
@patch("service.artefato_service.get_artefato_by_id", new_callable=AsyncMock)
def test_get_artefato_nao_encontrado(mock_get_one, mock_db): 
    mock_db.return_value = "fake_db"
    mock_get_one.return_value = None
    id_fake = str(uuid.uuid4())

    response = client.get(f"/artefatos/{id_fake}")

    assert response.status_code == 404
    assert f"Artefato com ID {id_fake} não encontrado" in response.json()["detail"]
    mock_get_one.assert_called_once()


@patch("routes.artefatos_router.get_db", new_callable=AsyncMock)
@patch("service.artefato_service.update_artefato", new_callable=AsyncMock)
def test_update_artefato(mock_update, mock_db): 
    artefato = artefatos_fake(1)[0]
    mock_db.return_value = "fake_db"
    updated_nome = "Nome Atualizado"

    artefato_atualizado = {
        "id": artefato["id"],
        "nome": updated_nome,
        "created_at": artefato["created_at"],
        "updated_at": datetime.now().isoformat()
    }
    mock_update.return_value = artefato_atualizado

    response = client.put(f"/artefatos/{artefato['id']}", json={
        "nome": updated_nome
    })

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == artefato["id"]
    assert data["nome"] == artefato_atualizado["nome"]


@patch("routes.artefatos_router.get_db", new_callable=AsyncMock)
@patch("service.artefato_service.delete_artefato", new_callable=AsyncMock)
def test_delete_artefato(mock_delete, mock_db):
    artefato = artefatos_fake(1)[0]
    mock_db.return_value = "fake_db"
    mock_delete.return_value = artefato

    response = client.delete(f"/artefatos/{artefato['id']}")

    assert response.status_code == 204
    assert response.text == ''
    mock_delete.assert_called_once()
