import pytest
from unittest.mock import patch, MagicMock, ANY
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
    from model.fase import FaseCreate, FaseUpdate, FaseResponse
    from service.fase_service import FaseService

client = TestClient(app)

def fases_fake(quant: int):
    lista = []
    for i in range(quant):
        lista.append({
            "id": str(uuid.uuid4()),
            "nome": f"Fase {i}",
            "descritivo": f"Descrição da fase {i}",
            "ordem": i + 1,
            "artefatos": []
        })
    return lista

@pytest.fixture
def fase_create():
    return FaseCreate(
        nome="Fase de Teste",
        descritivo="Descrição da fase de teste",
        ordem=1,
        artefato_ids=[]
    )

@pytest.fixture
def fase_update():
    return FaseUpdate(
        nome="Fase Atualizada",
        descritivo="Descrição atualizada",
        ordem=2,
        artefato_ids=[]
    )

# Testes de Criar Fase
@patch("service.fase_service.FaseService.create_fase")
def test_criar_fase(mock_create_fase, fase_create):
    fase_fake = fases_fake(1)[0]
    mock_create_fase.return_value = FaseResponse(
        id=fase_fake["id"],
        nome=fase_fake["nome"],
        descritivo=fase_fake["descritivo"],
        ordem=fase_fake["ordem"],
        artefatos=fase_fake["artefatos"]
    )
    
    response = client.post("/fases/", json=fase_create.model_dump())
    data = response.json()

    assert response.status_code == 201
    assert data["nome"] == fase_fake["nome"]
    assert data["descritivo"] == fase_fake["descritivo"]
    assert data["ordem"] == fase_fake["ordem"]
    assert "id" in data
    mock_create_fase.assert_called_once()

@patch("service.fase_service.FaseService.create_fase")
def test_criar_fase_erro(mock_create_fase, fase_create):
    mock_create_fase.return_value = None
    
    response = client.post("/fases/", json=fase_create.model_dump())

    assert response.status_code == 400
    assert "Erro ao criar a fase" in response.json()["detail"]

# Testes de Listar Fases
@patch("service.fase_service.FaseService.get_all_fases")
def test_listar_fases(mock_get_all_fases):
    fases_disponiveis = fases_fake(3)
    mock_get_all_fases.return_value = [
        FaseResponse(
            id=fase["id"],
            nome=fase["nome"],
            descritivo=fase["descritivo"],
            ordem=fase["ordem"],
            artefatos=fase["artefatos"]
        ) for fase in fases_disponiveis
    ]
    
    response = client.get("/fases/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 3
    assert data[0]["nome"] == fases_disponiveis[0]["nome"]
    assert data[0]["descritivo"] == fases_disponiveis[0]["descritivo"]
    assert data[0]["ordem"] == fases_disponiveis[0]["ordem"]
    mock_get_all_fases.assert_called_once()

@patch("service.fase_service.FaseService.get_all_fases")
def test_listar_fases_vazio(mock_get_all_fases):
    mock_get_all_fases.return_value = None
    
    response = client.get("/fases/")

    assert response.status_code == 404
    assert "Nenhuma fase encontrada" in response.json()["detail"]

# Testes de Obter Fase por ID
@patch("service.fase_service.FaseService.get_fase_by_id")
def test_obter_fase_por_id(mock_get_fase_by_id):
    fase_disponivel = fases_fake(1)[0]
    mock_get_fase_by_id.return_value = FaseResponse(
        id=fase_disponivel["id"],
        nome=fase_disponivel["nome"],
        descritivo=fase_disponivel["descritivo"],
        ordem=fase_disponivel["ordem"],
        artefatos=fase_disponivel["artefatos"]
    )
    
    response = client.get(f"/fases/{fase_disponivel['id']}")
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == fase_disponivel["id"]
    assert data["nome"] == fase_disponivel["nome"]
    assert data["descritivo"] == fase_disponivel["descritivo"]
    assert data["ordem"] == fase_disponivel["ordem"]
    mock_get_fase_by_id.assert_called_once()

@patch("service.fase_service.FaseService.get_fase_by_id")
def test_obter_fase_por_id_nao_encontrada(mock_get_fase_by_id):
    mock_get_fase_by_id.return_value = None
    fase_id = str(uuid.uuid4())
    
    response = client.get(f"/fases/{fase_id}")

    assert response.status_code == 404
    assert f"Fase com ID {fase_id} não encontrada" in response.json()["detail"]

# Testes de Atualizar Fase
@patch("service.fase_service.FaseService.update_fase")
def test_atualizar_fase(mock_update_fase, fase_update):
    fase_id = str(uuid.uuid4())
    fase_atualizada = fases_fake(1)[0]
    fase_atualizada["id"] = fase_id
    fase_atualizada["nome"] = "Fase Atualizada"
    fase_atualizada["descritivo"] = "Descrição atualizada"
    fase_atualizada["ordem"] = 2
    
    mock_update_fase.return_value = FaseResponse(
        id=fase_atualizada["id"],
        nome=fase_atualizada["nome"],
        descritivo=fase_atualizada["descritivo"],
        ordem=fase_atualizada["ordem"],
        artefatos=fase_atualizada["artefatos"]
    )
    
    response = client.put(f"/fases/{fase_id}", json=fase_update.model_dump())
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == fase_id
    assert data["nome"] == fase_atualizada["nome"]
    assert data["descritivo"] == fase_atualizada["descritivo"]
    assert data["ordem"] == fase_atualizada["ordem"]
    mock_update_fase.assert_called_once()

@patch("service.fase_service.FaseService.update_fase")
def test_atualizar_fase_nao_encontrada(mock_update_fase, fase_update):
    mock_update_fase.return_value = None
    fase_id = str(uuid.uuid4())
    
    response = client.put(f"/fases/{fase_id}", json=fase_update.model_dump())

    assert response.status_code == 404
    assert f"Fase com ID {fase_id} não encontrada para atualização" in response.json()["detail"]

# Testes de Deletar Fase
@patch("service.fase_service.FaseService.delete_fase")
def test_deletar_fase(mock_delete_fase):
    mock_delete_fase.return_value = True
    fase_id = str(uuid.uuid4())
    
    response = client.delete(f"/fases/{fase_id}")

    assert response.status_code == 204
    assert response.text == ''
    mock_delete_fase.assert_called_once()

@patch("service.fase_service.FaseService.delete_fase")
def test_deletar_fase_nao_encontrada(mock_delete_fase):
    mock_delete_fase.return_value = None
    fase_id = str(uuid.uuid4())
    
    response = client.delete(f"/fases/{fase_id}")

    assert response.status_code == 404
    assert f"Fase com ID {fase_id} não encontrada para deleção" in response.json()["detail"]

# Testes de Serviço (Unit tests)
def test_criar_fase_sucesso_service(mocker, fase_create):
    fake_id = str(uuid.uuid4())
    fake_fase_response = FaseResponse(
        id=fake_id,
        nome=fase_create.nome,
        descritivo=fase_create.descritivo,
        ordem=fase_create.ordem,
        artefatos=[]
    )

    mock_create = mocker.patch.object(
        FaseService,
        'create_fase',
        return_value=fake_fase_response
    )

    import asyncio
    result = asyncio.run(FaseService.create_fase(None, fase_create))
    
    assert result.nome == fase_create.nome
    assert result.descritivo == fase_create.descritivo
    assert result.ordem == fase_create.ordem
    assert hasattr(result, "id")

def test_criar_fase_erro_service(mocker, fase_create):
    mock_create = mocker.patch.object(
        FaseService,
        'create_fase',
        return_value=None
    )

    import asyncio
    result = asyncio.run(FaseService.create_fase(None, fase_create))
    
    assert result is None

def test_listar_fases_service(mocker):
    fases_disponiveis = fases_fake(3)
    fake_fases_response = [
        FaseResponse(
            id=fase["id"],
            nome=fase["nome"],
            descritivo=fase["descritivo"],
            ordem=fase["ordem"],
            artefatos=fase["artefatos"]
        ) for fase in fases_disponiveis
    ]

    mock_get_all = mocker.patch.object(
        FaseService,
        'get_all_fases',
        return_value=fake_fases_response
    )

    import asyncio
    result = asyncio.run(FaseService.get_all_fases(None))
    
    assert len(result) == 3
    assert result[0].nome == fases_disponiveis[0]["nome"]

def test_obter_fase_por_id_service(mocker):
    fase_disponivel = fases_fake(1)[0]
    fake_fase_response = FaseResponse(
        id=fase_disponivel["id"],
        nome=fase_disponivel["nome"],
        descritivo=fase_disponivel["descritivo"],
        ordem=fase_disponivel["ordem"],
        artefatos=fase_disponivel["artefatos"]
    )

    mock_get_by_id = mocker.patch.object(
        FaseService,
        'get_fase_by_id',
        return_value=fake_fase_response
    )

    import asyncio
    result = asyncio.run(FaseService.get_fase_by_id(None, fase_disponivel["id"]))
    
    assert result is not None
    assert result.id == fase_disponivel["id"]
    assert result.nome == fase_disponivel["nome"]
