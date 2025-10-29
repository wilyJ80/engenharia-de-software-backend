import pytest
from unittest.mock import patch
import uuid

from fastapi.testclient import TestClient
from main import app
from core.auth import get_current_user
from model.dto.usuario_dto import UsuarioCreateDTO, UsuarioResponseDTO
from routes.usuario_route import UsuarioService

client = TestClient(app)

def usuarios_fake(quant: int):
    lista = []
    for i in range(quant):
        lista.append({
            "id": str(uuid.uuid4()),
            "nome": f"usuario {i}",
            "email": f"email_teste{i}@email.com",
            #"senha_hash": f"hash_senha{i}",
        })
    return lista

@pytest.fixture
def usuario_base():
    return UsuarioCreateDTO(
        nome="Eduardo Américo",
        email="eduardo@example.com",
        senha="12345678"
    )

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


@patch("service.usuario_service.UsuarioService.get_user_by_id")
def test_acessar_usuario_unico(mock_get_user_by_id):  #usa autenticacao
    app.dependency_overrides[get_current_user] = lambda: "fake_user_id"

    user_disponivel = usuarios_fake(1)[0]
    mock_get_user_by_id.return_value = user_disponivel
    
    response = client.get(f"/usuarios/{user_disponivel['id']}")
    data = response.json()

    assert response.status_code == 200
    assert data == user_disponivel
    app.dependency_overrides = {}


@patch("service.usuario_service.UsuarioService.create_user")
@patch("service.usuario_service.UsuarioService.update_user")
def test_editar_usuario(mock_update_user, mock_create_user):  #usa autenticacao
    id_user_logado = "fake_user_id"
    app.dependency_overrides[get_current_user] = lambda: id_user_logado

    user_disponivel = usuarios_fake(1)[0]
    user_disponivel['id'] = id_user_logado
    mock_create_user.return_value = user_disponivel

    usuario_atualizado = {
        "id": id_user_logado,
        "nome": f"{user_disponivel['nome']}Atualizado",
        "email": f"{user_disponivel['email']}.br",
        "senha": "nova_senha123"
    }
    mock_update_user.return_value = usuario_atualizado

    response = client.put(f"/usuarios/{id_user_logado}", json=usuario_atualizado)
    data = response.json()

    assert response.status_code == 200
    assert data['id'] == id_user_logado
    assert data['nome'] == usuario_atualizado['nome']
    assert data['email'] == usuario_atualizado['email']
    app.dependency_overrides = {}


@patch("service.usuario_service.UsuarioService.delete_user")
def test_deletar_usuario(mock_delete_user):  #usa autenticacao
    id_user_logado = "fake_user_id"
    app.dependency_overrides[get_current_user] = lambda: id_user_logado

    mock_delete_user.return_value = True
    
    response = client.delete(f"/usuarios/{id_user_logado}")

    assert response.status_code == 204
    assert response.text == ''
    mock_delete_user.assert_called_once_with(id_user_logado)
    app.dependency_overrides = {}


@patch("service.usuario_service.UsuarioService.delete_user")
def test_deletar_usuario_sem_acesso(mock_delete_user):  #usa autenticacao
    id_user_logado = "fake_user_id"
    app.dependency_overrides[get_current_user] = lambda: id_user_logado

    mock_delete_user.return_value = True
    
    response = client.delete(f"/usuarios/id_outro_usuario")

    assert response.status_code == 403
    mock_delete_user.assert_not_called
    app.dependency_overrides = {}


def test_criar_usuario_sucesso(mocker, usuario_base):
    fake_id = "1234"
    fake_user = UsuarioResponseDTO(id=fake_id, nome=usuario_base.nome, email=usuario_base.email)

    mocker.patch.object(
        UsuarioService,
        'create_user',
        return_value=fake_user
    )

    usuario_resp = UsuarioService.create_user(usuario_base)
    assert usuario_resp.nome == usuario_base.nome
    assert usuario_resp.email == usuario_base.email
    assert hasattr(usuario_resp, "id")


def test_criar_usuario_email_duplicado(mocker, usuario_base):
    mocker.patch.object(
        UsuarioService,
        'create_user',
        side_effect=ValueError("Email já cadastrado")
    )

    with pytest.raises(ValueError, match="Email já cadastrado"):
        UsuarioService.create_user(usuario_base)

