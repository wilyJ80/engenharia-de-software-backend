from unittest.mock import patch
import pytest
import uuid

from fastapi.testclient import TestClient
from main import app
from core.auth import get_current_user

client = TestClient(app)

def usuarios_fake(quant: int):
    lista = []
    for i in range(quant):
        lista.append({
            "id": str(uuid.uuid4()),
            "nome": f"usuario {i}",
            "email": f"email_teste{i}@email.com",
            "senha_hash": f"hash_senha{i}",
        })
    return lista


def test_acesso_negado():
    response = client.get("/usuarios/")

    assert response.status_code == 403


@patch("service.usuario_service.UsuarioService.get_all_users")
def test_listar_usuarios(mock_get_all_users):  #usa autenticacao
    app.dependency_overrides[get_current_user] = lambda: "fake_user_id"
    
    users_disponiveis = usuarios_fake(2)
    mock_get_all_users.return_value = users_disponiveis
    
    response = client.get("/usuarios/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["email"] == users_disponiveis[0]["email"]
    assert data[1]["email"]== users_disponiveis[1]["email"]
    app.dependency_overrides = {}