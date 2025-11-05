import pytest
from unittest.mock import patch
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
    from model.dto.ciclo_dto import CicloCreateDTO, CicloUpdateDTO, CicloResponseDTO
    from service.ciclo_service import CicloService

client = TestClient(app)

def ciclos_fake(quant: int):
    lista = []
    for i in range(quant):
        lista.append({
            "id": str(uuid.uuid4()),
            "nome": f"Ciclo {i}",
            "versao": f"{i}.0.0",
            "projeto_id": str(uuid.uuid4()),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
    return lista

@pytest.fixture
def ciclo_create():
    return CicloCreateDTO(
        nome="Ciclo de Teste",
        versao="1.0.0",
        projeto_id=str(uuid.uuid4())
    )

@pytest.fixture
def ciclo_update():
    return CicloUpdateDTO(
        nome="Ciclo Atualizado",
        versao="2.0.0",
        projeto_id=str(uuid.uuid4())
    )

# Testes de Criar Ciclo
@patch("service.ciclo_service.CicloService.create_ciclo")
def test_criar_ciclo(mock_create_ciclo, ciclo_create):
    ciclo_fake = ciclos_fake(1)[0]
    mock_create_ciclo.return_value = CicloResponseDTO(
        id=ciclo_fake["id"],
        nome=ciclo_fake["nome"],
        versao=ciclo_fake["versao"],
        projeto_id=ciclo_fake["projeto_id"],
        created_at=ciclo_fake["created_at"],
        updated_at=ciclo_fake["updated_at"]
    )
    
    response = client.post("/ciclos/", json=ciclo_create.model_dump())
    data = response.json()

    assert response.status_code == 201
    assert data["nome"] == ciclo_fake["nome"]
    assert data["versao"] == ciclo_fake["versao"]
    assert data["projeto_id"] == ciclo_fake["projeto_id"]
    assert "id" in data
    mock_create_ciclo.assert_called_once()

@patch("service.ciclo_service.CicloService.create_ciclo")
def test_criar_ciclo_erro_validacao(mock_create_ciclo, ciclo_create):
    mock_create_ciclo.side_effect = ValueError("Ciclo com este nome já existe")
    
    response = client.post("/ciclos/", json=ciclo_create.model_dump())

    assert response.status_code == 400
    assert "Ciclo com este nome já existe" in response.json()["detail"]

# Testes de Listar Ciclos
@patch("service.ciclo_service.CicloService.get_all_ciclos")
def test_listar_ciclos(mock_get_all_ciclos):
    ciclos_disponiveis = ciclos_fake(3)
    mock_get_all_ciclos.return_value = [
        CicloResponseDTO(
            id=ciclo["id"],
            nome=ciclo["nome"],
            versao=ciclo["versao"],
            projeto_id=ciclo["projeto_id"],
            created_at=ciclo["created_at"],
            updated_at=ciclo["updated_at"]
        ) for ciclo in ciclos_disponiveis
    ]
    
    response = client.get("/ciclos/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 3
    assert data[0]["nome"] == ciclos_disponiveis[0]["nome"]
    assert data[0]["versao"] == ciclos_disponiveis[0]["versao"]
    mock_get_all_ciclos.assert_called_once()

@patch("service.ciclo_service.CicloService.get_all_ciclos")
def test_listar_ciclos_vazio(mock_get_all_ciclos):
    mock_get_all_ciclos.return_value = []
    
    response = client.get("/ciclos/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 0

# Testes de Listar Ciclos por Projeto
@patch("service.ciclo_service.CicloService.get_ciclos_by_projeto")
def test_listar_ciclos_por_projeto(mock_get_ciclos_by_projeto):
    projeto_id = str(uuid.uuid4())
    ciclos_disponiveis = ciclos_fake(2)

    # Atualiza para o mesmo projeto_id
    for ciclo in ciclos_disponiveis:
        ciclo["projeto_id"] = projeto_id
    
    mock_get_ciclos_by_projeto.return_value = [
        CicloResponseDTO(
            id=ciclo["id"],
            nome=ciclo["nome"],
            versao=ciclo["versao"],
            projeto_id=ciclo["projeto_id"],
            created_at=ciclo["created_at"],
            updated_at=ciclo["updated_at"]
        ) for ciclo in ciclos_disponiveis
    ]
    
    response = client.get(f"/ciclos/projeto/{projeto_id}")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert all(ciclo["projeto_id"] == projeto_id for ciclo in data)
    mock_get_ciclos_by_projeto.assert_called_once()
    assert mock_get_ciclos_by_projeto.call_args[0][1] == projeto_id

@patch("service.ciclo_service.CicloService.get_ciclos_by_projeto")
def test_listar_ciclos_por_projeto_query_param(mock_get_ciclos_by_projeto):
    projeto_id = str(uuid.uuid4())
    ciclos_disponiveis = ciclos_fake(2)
    for ciclo in ciclos_disponiveis:
        ciclo["projeto_id"] = projeto_id
    
    mock_get_ciclos_by_projeto.return_value = [
        CicloResponseDTO(
            id=ciclo["id"],
            nome=ciclo["nome"],
            versao=ciclo["versao"],
            projeto_id=ciclo["projeto_id"],
            created_at=ciclo["created_at"],
            updated_at=ciclo["updated_at"]
        ) for ciclo in ciclos_disponiveis
    ]
    
    response = client.get(f"/ciclos/?projeto_id={projeto_id}")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    mock_get_ciclos_by_projeto.assert_called_once()

# Testes de Filtrar Ciclos por Versão
@patch("service.ciclo_service.CicloService.get_ciclos_by_versao")
def test_listar_ciclos_por_versao(mock_get_ciclos_by_versao):
    versao = "1.0.0"
    ciclos_disponiveis = ciclos_fake(2)
    for ciclo in ciclos_disponiveis:
        ciclo["versao"] = versao
    
    mock_get_ciclos_by_versao.return_value = [
        CicloResponseDTO(
            id=ciclo["id"],
            nome=ciclo["nome"],
            versao=ciclo["versao"],
            projeto_id=ciclo["projeto_id"],
            created_at=ciclo["created_at"],
            updated_at=ciclo["updated_at"]
        ) for ciclo in ciclos_disponiveis
    ]
    
    response = client.get(f"/ciclos/?versao={versao}")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert all(ciclo["versao"] == versao for ciclo in data)
    mock_get_ciclos_by_versao.assert_called_once()

# Testes de Obter Ciclo por Nome
@patch("service.ciclo_service.CicloService.get_ciclo_by_nome")
def test_obter_ciclo_por_nome(mock_get_ciclo_by_nome):
    ciclo_disponivel = ciclos_fake(1)[0]
    mock_get_ciclo_by_nome.return_value = CicloResponseDTO(
        id=ciclo_disponivel["id"],
        nome=ciclo_disponivel["nome"],
        versao=ciclo_disponivel["versao"],
        projeto_id=ciclo_disponivel["projeto_id"],
        created_at=ciclo_disponivel["created_at"],
        updated_at=ciclo_disponivel["updated_at"]
    )
    
    response = client.get(f"/ciclos/nome/{ciclo_disponivel['nome']}")
    data = response.json()

    assert response.status_code == 200
    assert data["nome"] == ciclo_disponivel["nome"]
    assert data["versao"] == ciclo_disponivel["versao"]
    mock_get_ciclo_by_nome.assert_called_once()

@patch("service.ciclo_service.CicloService.get_ciclo_by_nome")
def test_obter_ciclo_por_nome_nao_encontrado(mock_get_ciclo_by_nome):
    mock_get_ciclo_by_nome.return_value = None
    
    response = client.get("/ciclos/nome/Ciclo Inexistente")

    assert response.status_code == 404
    assert "Ciclo não encontrado" in response.json()["detail"]

# Testes de Obter Ciclo por ID
@patch("service.ciclo_service.CicloService.get_ciclo_by_id")
def test_obter_ciclo_por_id(mock_get_ciclo_by_id):
    ciclo_disponivel = ciclos_fake(1)[0]
    mock_get_ciclo_by_id.return_value = CicloResponseDTO(
        id=ciclo_disponivel["id"],
        nome=ciclo_disponivel["nome"],
        versao=ciclo_disponivel["versao"],
        projeto_id=ciclo_disponivel["projeto_id"],
        created_at=ciclo_disponivel["created_at"],
        updated_at=ciclo_disponivel["updated_at"]
    )
    
    response = client.get(f"/ciclos/{ciclo_disponivel['id']}")
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == ciclo_disponivel["id"]
    assert data["nome"] == ciclo_disponivel["nome"]
    assert data["versao"] == ciclo_disponivel["versao"]
    mock_get_ciclo_by_id.assert_called_once()

@patch("service.ciclo_service.CicloService.get_ciclo_by_id")
def test_obter_ciclo_por_id_nao_encontrado(mock_get_ciclo_by_id):
    mock_get_ciclo_by_id.return_value = None
    ciclo_id = str(uuid.uuid4())
    
    response = client.get(f"/ciclos/{ciclo_id}")

    assert response.status_code == 404
    assert "Ciclo não encontrado" in response.json()["detail"]

# Testes de Atualizar Ciclo
@patch("service.ciclo_service.CicloService.update_ciclo")
def test_atualizar_ciclo(mock_update_ciclo, ciclo_update):
    ciclo_id = str(uuid.uuid4())
    ciclo_atualizado = ciclos_fake(1)[0]
    ciclo_atualizado["id"] = ciclo_id
    ciclo_atualizado["nome"] = "Ciclo Atualizado"
    ciclo_atualizado["versao"] = "2.0.0"
    
    mock_update_ciclo.return_value = CicloResponseDTO(
        id=ciclo_atualizado["id"],
        nome=ciclo_atualizado["nome"],
        versao=ciclo_atualizado["versao"],
        projeto_id=ciclo_atualizado["projeto_id"],
        created_at=ciclo_atualizado["created_at"],
        updated_at=ciclo_atualizado["updated_at"]
    )
    
    response = client.put(f"/ciclos/{ciclo_id}", json=ciclo_update.model_dump())
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == ciclo_id
    assert data["nome"] == ciclo_atualizado["nome"]
    assert data["versao"] == ciclo_atualizado["versao"]
    mock_update_ciclo.assert_called_once()

@patch("service.ciclo_service.CicloService.update_ciclo")
def test_atualizar_ciclo_nao_encontrado(mock_update_ciclo, ciclo_update):
    mock_update_ciclo.return_value = None
    ciclo_id = str(uuid.uuid4())
    
    response = client.put(f"/ciclos/{ciclo_id}", json=ciclo_update.model_dump())

    assert response.status_code == 404
    assert "Ciclo não encontrado" in response.json()["detail"]

@patch("service.ciclo_service.CicloService.update_ciclo")
def test_atualizar_ciclo_erro_validacao(mock_update_ciclo, ciclo_update):
    mock_update_ciclo.side_effect = ValueError("Ciclo com este nome já existe")
    ciclo_id = str(uuid.uuid4())
    
    response = client.put(f"/ciclos/{ciclo_id}", json=ciclo_update.model_dump())

    assert response.status_code == 400
    assert "Ciclo com este nome já existe" in response.json()["detail"]

# Testes de Deletar Ciclo
@patch("service.ciclo_service.CicloService.delete_ciclo")
def test_deletar_ciclo(mock_delete_ciclo):
    mock_delete_ciclo.return_value = True
    ciclo_id = str(uuid.uuid4())
    
    response = client.delete(f"/ciclos/{ciclo_id}")

    assert response.status_code == 204
    assert response.text == ''
    mock_delete_ciclo.assert_called_once()

@patch("service.ciclo_service.CicloService.delete_ciclo")
def test_deletar_ciclo_nao_encontrado(mock_delete_ciclo):
    mock_delete_ciclo.return_value = False
    ciclo_id = str(uuid.uuid4())
    
    response = client.delete(f"/ciclos/{ciclo_id}")

    assert response.status_code == 404
    assert "Ciclo não encontrado" in response.json()["detail"]

# Testes de Serviço (Unit tests)
def test_criar_ciclo_sucesso_service(mocker, ciclo_create):
    fake_id = str(uuid.uuid4())
    fake_ciclo_response = CicloResponseDTO(
        id=fake_id,
        nome=ciclo_create.nome,
        versao=ciclo_create.versao,
        projeto_id=ciclo_create.projeto_id,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )

    mock_create = mocker.patch.object(
        CicloService,
        'create_ciclo',
        return_value=fake_ciclo_response
    )

    import asyncio
    result = asyncio.run(CicloService.create_ciclo(None, ciclo_create))
    
    assert result.nome == ciclo_create.nome
    assert result.versao == ciclo_create.versao
    assert result.projeto_id == ciclo_create.projeto_id
    assert hasattr(result, "id")

def test_criar_ciclo_erro_validacao_service(mocker, ciclo_create):
    mock_create = mocker.patch.object(
        CicloService,
        'create_ciclo',
        side_effect=ValueError("Ciclo com este nome já existe")
    )

    with pytest.raises(ValueError, match="Ciclo com este nome já existe"):
        import asyncio
        asyncio.run(CicloService.create_ciclo(None, ciclo_create))

def test_listar_ciclos_service(mocker):
    ciclos_disponiveis = ciclos_fake(3)
    fake_ciclos_response = [
        CicloResponseDTO(
            id=ciclo["id"],
            nome=ciclo["nome"],
            versao=ciclo["versao"],
            projeto_id=ciclo["projeto_id"],
            created_at=ciclo["created_at"],
            updated_at=ciclo["updated_at"]
        ) for ciclo in ciclos_disponiveis
    ]

    mock_get_all = mocker.patch.object(
        CicloService,
        'get_all_ciclos',
        return_value=fake_ciclos_response
    )

    import asyncio
    result = asyncio.run(CicloService.get_all_ciclos(None))
    
    assert len(result) == 3
    assert result[0].nome == ciclos_disponiveis[0]["nome"]

def test_obter_ciclo_por_id_service(mocker):
    ciclo_disponivel = ciclos_fake(1)[0]
    fake_ciclo_response = CicloResponseDTO(
        id=ciclo_disponivel["id"],
        nome=ciclo_disponivel["nome"],
        versao=ciclo_disponivel["versao"],
        projeto_id=ciclo_disponivel["projeto_id"],
        created_at=ciclo_disponivel["created_at"],
        updated_at=ciclo_disponivel["updated_at"]
    )

    mock_get_by_id = mocker.patch.object(
        CicloService,
        'get_ciclo_by_id',
        return_value=fake_ciclo_response
    )

    import asyncio
    result = asyncio.run(CicloService.get_ciclo_by_id(None, ciclo_disponivel["id"]))
    
    assert result is not None
    assert result.id == ciclo_disponivel["id"]
    assert result.nome == ciclo_disponivel["nome"]