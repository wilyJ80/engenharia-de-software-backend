import pytest
from unittest.mock import patch, MagicMock
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
    from model.dto.usuario_dto import UsuarioCreateDTO, UsuarioLoginDTO, UsuarioResponseDTO
    from service.usuario_service import UsuarioService

client = TestClient(app)

def setup_auth_mock():
    """Helper function to setup authentication mock"""
    from core.auth import get_current_user
    
    def mock_get_current_user():
        return str(uuid.uuid4())
    
    app.dependency_overrides[get_current_user] = mock_get_current_user

def teardown_auth_mock():
    """Helper function to cleanup authentication mock"""
    app.dependency_overrides = {}

def usuarios_fake(quant: int):
    lista = []
    for i in range(quant):
        lista.append({
            "id": str(uuid.uuid4()),
            "nome": f"Usuario {i}",
            "email": f"usuario{i}@email.com",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
    return lista

@pytest.fixture
def usuario_create():
    return UsuarioCreateDTO(
        nome="Usuario de Teste",
        email="teste@email.com"
    )

@pytest.fixture
def usuario_login():
    return UsuarioLoginDTO(
        email="teste@email.com",
        senha="123"
    )

# Testes de Registro de Usuário
@patch("service.usuario_service.UsuarioService.create_user")
def test_criar_usuario(mock_create_user, usuario_create):
    usuario_fake = usuarios_fake(1)[0]
    mock_create_user.return_value = UsuarioResponseDTO(
        id=usuario_fake["id"],
        nome=usuario_fake["nome"],
        email=usuario_fake["email"]
    )
    
    response = client.post("/usuarios/registro", json=usuario_create.model_dump())
    data = response.json()

    assert response.status_code == 201
    assert data["nome"] == usuario_fake["nome"]
    assert data["email"] == usuario_fake["email"]
    assert "id" in data
    mock_create_user.assert_called_once()

@patch("service.usuario_service.UsuarioService.create_user")
def test_criar_usuario_email_duplicado(mock_create_user, usuario_create):
    mock_create_user.side_effect = ValueError("Email já cadastrado")
    
    response = client.post("/usuarios/registro", json=usuario_create.model_dump())

    assert response.status_code == 400
    assert "Email já cadastrado" in response.json()["detail"]

# Testes de Login
@patch("service.usuario_service.UsuarioService.authenticate_user")
def test_login_usuario_sucesso(mock_authenticate_user, usuario_login):
    from model.usuario import Usuario
    usuario_fake = usuarios_fake(1)[0]
    
    # Mock do usuário autenticado
    mock_user = Usuario(
        id=usuario_fake["id"],
        nome=usuario_fake["nome"],
        email=usuario_fake["email"],
        senha="123",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    mock_authenticate_user.return_value = mock_user
    
    with patch("core.auth.create_access_token") as mock_create_token:
        mock_create_token.return_value = "fake_token"
        
        response = client.post("/usuarios/login", json=usuario_login.model_dump())
        data = response.json()

        assert response.status_code == 200
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        mock_authenticate_user.assert_called_once()

@patch("service.usuario_service.UsuarioService.authenticate_user")
def test_login_usuario_credenciais_invalidas(mock_authenticate_user, usuario_login):
    mock_authenticate_user.return_value = None
    
    response = client.post("/usuarios/login", json=usuario_login.model_dump())

    assert response.status_code == 401
    assert "Email ou senha incorretos" in response.json()["detail"]

# Testes de Obter Usuário Atual
@patch("service.usuario_service.UsuarioService.get_user_by_id")
def test_obter_usuario_atual(mock_get_user_by_id):
    setup_auth_mock()
    
    usuario_fake = usuarios_fake(1)[0]
    mock_get_user_by_id.return_value = UsuarioResponseDTO(
        id=usuario_fake["id"],
        nome=usuario_fake["nome"],
        email=usuario_fake["email"]
    )
    
    response = client.get("/usuarios/me")
    data = response.json()

    assert response.status_code == 200
    assert data["nome"] == usuario_fake["nome"]
    assert data["email"] == usuario_fake["email"]
    mock_get_user_by_id.assert_called_once()
    
    teardown_auth_mock()

@patch("service.usuario_service.UsuarioService.get_user_by_id")
def test_obter_usuario_atual_nao_encontrado(mock_get_user_by_id):
    setup_auth_mock()
    
    mock_get_user_by_id.return_value = None
    
    response = client.get("/usuarios/me")

    assert response.status_code == 404
    assert "Usuário não encontrado" in response.json()["detail"]
    
    teardown_auth_mock()

# Testes de Listar Usuários
@patch("service.usuario_service.UsuarioService.get_all_users")
def test_listar_usuarios(mock_get_all_users):
    setup_auth_mock()
    
    usuarios_disponiveis = usuarios_fake(3)
    mock_get_all_users.return_value = [
        UsuarioResponseDTO(
            id=user["id"],
            nome=user["nome"],
            email=user["email"]
        ) for user in usuarios_disponiveis
    ]
    
    response = client.get("/usuarios/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 3
    assert data[0]["nome"] == usuarios_disponiveis[0]["nome"]
    assert data[0]["email"] == usuarios_disponiveis[0]["email"]
    mock_get_all_users.assert_called_once()
    
    teardown_auth_mock()

@patch("service.usuario_service.UsuarioService.get_all_users")
def test_listar_usuarios_vazio(mock_get_all_users):
    setup_auth_mock()
    
    mock_get_all_users.return_value = []
    
    response = client.get("/usuarios/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 0
    
    teardown_auth_mock()

# Testes de Obter Usuário por ID
@patch("service.usuario_service.UsuarioService.get_user_by_id")
def test_obter_usuario_por_id(mock_get_user_by_id):
    setup_auth_mock()
    
    usuario_disponivel = usuarios_fake(1)[0]
    mock_get_user_by_id.return_value = UsuarioResponseDTO(
        id=usuario_disponivel["id"],
        nome=usuario_disponivel["nome"],
        email=usuario_disponivel["email"]
    )
    
    response = client.get(f"/usuarios/{usuario_disponivel['id']}")
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == usuario_disponivel["id"]
    assert data["nome"] == usuario_disponivel["nome"]
    assert data["email"] == usuario_disponivel["email"]
    mock_get_user_by_id.assert_called_once()
    
    teardown_auth_mock()

@patch("service.usuario_service.UsuarioService.get_user_by_id")
def test_obter_usuario_por_id_nao_encontrado(mock_get_user_by_id):
    setup_auth_mock()
    
    mock_get_user_by_id.return_value = None
    user_id = str(uuid.uuid4())
    
    response = client.get(f"/usuarios/{user_id}")

    assert response.status_code == 404
    assert "Usuário não encontrado" in response.json()["detail"]
    
    teardown_auth_mock()

# Testes de Atualizar Usuário
@patch("service.usuario_service.UsuarioService.update_user")
def test_atualizar_usuario(mock_update_user, usuario_create):
    setup_auth_mock()
    
    user_id = str(uuid.uuid4())
    usuario_atualizado = {
        "id": user_id,
        "nome": "Usuario Atualizado",
        "email": "atualizado@email.com"
    }
    mock_update_user.return_value = UsuarioResponseDTO(
        id=usuario_atualizado["id"],
        nome=usuario_atualizado["nome"],
        email=usuario_atualizado["email"]
    )
    
    response = client.put(f"/usuarios/{user_id}", json=usuario_create.model_dump())
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == user_id
    assert data["nome"] == usuario_atualizado["nome"]
    assert data["email"] == usuario_atualizado["email"]
    mock_update_user.assert_called_once()
    
    teardown_auth_mock()

@patch("service.usuario_service.UsuarioService.update_user")
def test_atualizar_usuario_nao_encontrado(mock_update_user, usuario_create):
    setup_auth_mock()
    
    mock_update_user.return_value = None
    user_id = str(uuid.uuid4())
    
    response = client.put(f"/usuarios/{user_id}", json=usuario_create.model_dump())

    assert response.status_code == 404
    assert "Usuário não encontrado" in response.json()["detail"]
    
    teardown_auth_mock()

@patch("service.usuario_service.UsuarioService.update_user")
def test_atualizar_usuario_email_duplicado(mock_update_user, usuario_create):
    setup_auth_mock()
    
    mock_update_user.side_effect = ValueError("Email já cadastrado")
    user_id = str(uuid.uuid4())
    
    response = client.put(f"/usuarios/{user_id}", json=usuario_create.model_dump())

    assert response.status_code == 400
    assert "Email já cadastrado" in response.json()["detail"]
    
    teardown_auth_mock()

# Testes de Deletar Usuário
@patch("service.usuario_service.UsuarioService.delete_user")
def test_deletar_usuario(mock_delete_user):
    setup_auth_mock()
    
    mock_delete_user.return_value = True
    user_id = str(uuid.uuid4())
    
    response = client.delete(f"/usuarios/{user_id}")

    assert response.status_code == 204
    assert response.text == ''
    mock_delete_user.assert_called_once()
    
    teardown_auth_mock()

@patch("service.usuario_service.UsuarioService.delete_user")
def test_deletar_usuario_nao_encontrado(mock_delete_user):
    setup_auth_mock()
    
    mock_delete_user.return_value = False
    user_id = str(uuid.uuid4())
    
    response = client.delete(f"/usuarios/{user_id}")

    assert response.status_code == 404
    assert "Usuário não encontrado" in response.json()["detail"]
    
    teardown_auth_mock()

# Testes de Serviço (Unit tests)
def test_criar_usuario_sucesso_service(mocker, usuario_create):
    fake_id = str(uuid.uuid4())
    fake_usuario_response = UsuarioResponseDTO(
        id=fake_id,
        nome=usuario_create.nome,
        email=usuario_create.email
    )

    mock_create = mocker.patch.object(
        UsuarioService,
        'create_user',
        return_value=fake_usuario_response
    )

    # Como é uma função async, precisamos simular o comportamento
    import asyncio
    result = asyncio.run(UsuarioService.create_user(None, usuario_create))
    
    assert result.nome == usuario_create.nome
    assert result.email == usuario_create.email
    assert hasattr(result, "id")

def test_criar_usuario_email_duplicado_service(mocker, usuario_create):
    mock_create = mocker.patch.object(
        UsuarioService,
        'create_user',
        side_effect=ValueError("Email já cadastrado")
    )

    with pytest.raises(ValueError, match="Email já cadastrado"):
        import asyncio
        asyncio.run(UsuarioService.create_user(None, usuario_create))

def test_autenticar_usuario_sucesso_service(mocker, usuario_login):
    from model.usuario import Usuario
    fake_usuario = Usuario(
        id=str(uuid.uuid4()),
        nome="Test User",
        email=usuario_login.email,
        senha="123",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    mock_auth = mocker.patch.object(
        UsuarioService,
        'authenticate_user',
        return_value=fake_usuario
    )

    import asyncio
    result = asyncio.run(UsuarioService.authenticate_user(None, usuario_login.email, usuario_login.senha))
    
    assert result is not None
    assert result.email == usuario_login.email

def test_autenticar_usuario_credenciais_invalidas_service(mocker, usuario_login):
    mock_auth = mocker.patch.object(
        UsuarioService,
        'authenticate_user',
        return_value=None
    )

    import asyncio
    result = asyncio.run(UsuarioService.authenticate_user(None, "wrong@email.com", "wrong_password"))
    
    assert result is None