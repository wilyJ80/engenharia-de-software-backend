import pytest
from unittest.mock import AsyncMock, patch, MagicMock
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

def projetos_fake(quant: int):
    lista = []
    for i in range(quant):
        lista.append({
            "id": str(uuid.uuid4()),
            "nome": f"Projeto {i}",
            "descritivo": f"Descrição do projeto {i}",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
    return lista


@patch("routes.projeto_router.get_db", new_callable=AsyncMock)
@patch("service.projeto_service.ProjetoService.create_projeto", new_callable=AsyncMock)
def test_create_projeto(mock_create, mock_db):
    projeto = projetos_fake(1)[0]
    mock_db.return_value = "fake_db"
    mock_create.return_value = projeto

    response = client.post("/projetos/", json={
        "nome": projeto["nome"],
        "descritivo": projeto["descritivo"]
    })

    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == projeto["nome"]
    assert data["descritivo"] == projeto["descritivo"]


@patch("routes.projeto_router.get_db", new_callable=AsyncMock)
@patch("service.projeto_service.ProjetoService.get_all_projetos", new_callable=AsyncMock)
def test_get_all_projetos(mock_get_all, mock_db):
    projetos = projetos_fake(5)
    mock_db.return_value = "fake_db"
    mock_get_all.return_value = projetos

    response = client.get("/projetos/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert data == projetos


@patch("routes.projeto_router.get_db", new_callable=AsyncMock)
@patch("service.projeto_service.ProjetoService.get_projeto_by_id", new_callable=AsyncMock)
def test_get_projeto_by_id(mock_get_one, mock_db):
    projeto = projetos_fake(1)[0]
    mock_db.return_value = "fake_db"
    mock_get_one.return_value = projeto

    response = client.get(f"/projetos/{projeto['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == projeto["id"]
    assert data["nome"] == projeto["nome"]
    assert data["descritivo"] == projeto["descritivo"]


@patch("routes.projeto_router.get_db", new_callable=AsyncMock)
@patch("service.projeto_service.ProjetoService.get_all_projetos", new_callable=AsyncMock)
def test_update_projeto(mock_update, mock_db):
    pass


@patch("routes.projeto_router.get_db", new_callable=AsyncMock)
@patch("service.projeto_service.ProjetoService.get_all_projetos", new_callable=AsyncMock)
def test_delete_projeto(mock_delete, mock_db):
    pass


#ver um nao existente

