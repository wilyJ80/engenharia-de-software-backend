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
@patch("service.projeto_service.ProjetoService.get_projeto_by_id", new_callable=AsyncMock)
def test_get_projeto_nao_encontrado(mock_get_one, mock_db):
    mock_db.return_value = "fake_db"
    mock_get_one.return_value = None
    id_fake = str(uuid.uuid4())

    response = client.get(f"/projetos/{id_fake}")

    assert response.status_code == 404
    assert "Projeto não encontrado" in response.json()["detail"]
    mock_get_one.assert_called_once


@patch("routes.projeto_router.get_db", new_callable=AsyncMock)
@patch("service.projeto_service.ProjetoService.update_projeto", new_callable=AsyncMock)
def test_update_projeto(mock_update, mock_db):
    projeto = projetos_fake(1)[0]
    updated_nome = "Nome Atualizado"
    updated_descritivo = "Descrição Atualizada"

    projeto_atualizado = {
        "id": projeto["id"],
        "nome": updated_nome,
        "descritivo": updated_descritivo,
        "created_at": projeto["created_at"],
        "updated_at": datetime.now().isoformat()
    }


    mock_db.return_value = "fake_db"
    mock_update.return_value = projeto_atualizado

    response = client.put(f"/projetos/{projeto['id']}", json={
        "nome": updated_nome,
        "descritivo": updated_descritivo
    })

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == projeto["id"]
    assert data["nome"] == updated_nome
    assert data["descritivo"] == updated_descritivo
    assert data["updated_at"] != projeto["updated_at"]
    assert data["created_at"] == projeto["created_at"]


@patch("routes.projeto_router.get_db", new_callable=AsyncMock)
@patch("service.projeto_service.ProjetoService.delete_projeto", new_callable=AsyncMock)
def test_delete_projeto(mock_delete, mock_db):
    projeto = projetos_fake(1)[0]
    mock_db.return_value = "fake_db"
    mock_delete.return_value = projeto

    response = client.delete(f"/projetos/{projeto['id']}")

    assert response.status_code == 204
    assert response.text == ''
    mock_delete.assert_called_once()


#ver um nao existente

