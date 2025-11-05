import pytest
from unittest.mock import patch, ANY
import uuid
import os
import sys

# Adiciona o diretório src ao sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

# Mock das conexões de banco antes de importar a aplicação
with patch('db.connection.Connection'):
    from fastapi.testclient import TestClient
    from main import app
    from model.dto.card_dto import CardCreateDTO, CardUpdateDTO, CardResponseDTO
    from model.card_status import CardStatus
    from service.card_service import CardService

client = TestClient(app)

def cards_fake(quant: int):
    lista = []
    for i in range(quant):
        lista.append({
            "id": str(uuid.uuid4()),
            "status": CardStatus.A_FAZER.value,
            "tempo_planejado_horas": 4.5 + i,
            "link": f"http://exemplo.com/card/{i}",
            "descricao": f"Descrição do card {i}",
            "ciclo_id": str(uuid.uuid4()),
            "fase_id": str(uuid.uuid4()),
            "artefato_id": str(uuid.uuid4()),
            "responsavel_id": str(uuid.uuid4())
        })
    return lista

@pytest.fixture
def card_create():
    return CardCreateDTO(
        status=CardStatus.A_FAZER.value,
        tempo_planejado_horas=5.0,
        link="http://exemplo.com/tarefa/123",
        descricao="Implementar funcionalidade de teste",
        ciclo_id=str(uuid.uuid4()),
        fase_id=str(uuid.uuid4()),
        artefato_id=str(uuid.uuid4()),
        responsavel_id=str(uuid.uuid4())
    )

@pytest.fixture
def card_update():
    return CardUpdateDTO(
        status="em_andamento",
        tempo_planejado_horas=8.0,
        link="http://exemplo.com/tarefa/123/atualizado",
        descricao="Implementar funcionalidade de teste com validações"
    )

# Testes de Criar Card
@patch("service.card_service.CardService.create_card")
def test_criar_card(mock_create_card, card_create):
    card_fake = cards_fake(1)[0]
    mock_create_card.return_value = CardResponseDTO(
        id=card_fake["id"],
        status=card_fake["status"],
        tempo_planejado_horas=card_fake["tempo_planejado_horas"],
        link=card_fake["link"],
        descricao=card_fake["descricao"],
        ciclo_id=card_fake["ciclo_id"],
        fase_id=card_fake["fase_id"],
        artefato_id=card_fake["artefato_id"],
        responsavel_id=card_fake["responsavel_id"]
    )
    
    response = client.post("/card/", json=card_create.model_dump())
    data = response.json()

    assert response.status_code == 201
    assert data["status"] == card_fake["status"]
    assert data["tempo_planejado_horas"] == card_fake["tempo_planejado_horas"]
    assert data["link"] == card_fake["link"]
    assert data["descricao"] == card_fake["descricao"]
    assert "id" in data
    mock_create_card.assert_called_once()

@patch("service.card_service.CardService.create_card")
def test_criar_card_erro_validacao(mock_create_card, card_create):
    mock_create_card.side_effect = ValueError("Ciclo não encontrado")
    
    response = client.post("/card/", json=card_create.model_dump())

    assert response.status_code == 400
    assert "Ciclo não encontrado" in response.json()["detail"]

# Testes de Listar Cards
@patch("service.card_service.CardService.get_all_cards")
def test_listar_cards(mock_get_all_cards):
    cards_disponiveis = cards_fake(3)
    mock_get_all_cards.return_value = [
        CardResponseDTO(
            id=card["id"],
            status=card["status"],
            tempo_planejado_horas=card["tempo_planejado_horas"],
            link=card["link"],
            descricao=card["descricao"],
            ciclo_id=card["ciclo_id"],
            fase_id=card["fase_id"],
            artefato_id=card["artefato_id"],
            responsavel_id=card["responsavel_id"]
        ) for card in cards_disponiveis
    ]
    
    response = client.get("/card/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 3
    assert data[0]["descricao"] == cards_disponiveis[0]["descricao"]
    assert data[0]["tempo_planejado_horas"] == cards_disponiveis[0]["tempo_planejado_horas"]
    mock_get_all_cards.assert_called_once()

@patch("service.card_service.CardService.get_all_cards")
def test_listar_cards_vazio(mock_get_all_cards):
    mock_get_all_cards.return_value = []
    
    response = client.get("/card/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 0

# Testes de Listar Cards por Status
@patch("service.card_service.CardService.get_cards_by_status")
def test_listar_cards_por_status(mock_get_cards_by_status):
    status_filtro = CardStatus.EM_ANDAMENTO.value
    cards_disponiveis = cards_fake(2)
    for card in cards_disponiveis:
        card["status"] = status_filtro
    
    mock_get_cards_by_status.return_value = [
        CardResponseDTO(
            id=card["id"],
            status=card["status"],
            tempo_planejado_horas=card["tempo_planejado_horas"],
            link=card["link"],
            descricao=card["descricao"],
            ciclo_id=card["ciclo_id"],
            fase_id=card["fase_id"],
            artefato_id=card["artefato_id"],
            responsavel_id=card["responsavel_id"]
        ) for card in cards_disponiveis
    ]
    
    response = client.get(f"/card/?status_filtro={status_filtro}")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2
    assert all(card["status"] == status_filtro for card in data)
    mock_get_cards_by_status.assert_called_once()

# Testes de Listar Cards por Ciclo
@patch("service.card_service.CardService.get_cards_by_ciclo")
def test_listar_cards_por_ciclo(mock_get_cards_by_ciclo):
    ciclo_id = str(uuid.uuid4())
    cards_disponiveis = cards_fake(2)
    for card in cards_disponiveis:
        card["ciclo_id"] = ciclo_id
    
    mock_get_cards_by_ciclo.return_value = [
        CardResponseDTO(
            id=card["id"],
            status=card["status"],
            tempo_planejado_horas=card["tempo_planejado_horas"],
            link=card["link"],
            descricao=card["descricao"],
            ciclo_id=card["ciclo_id"],
            fase_id=card["fase_id"],
            artefato_id=card["artefato_id"],
            responsavel_id=card["responsavel_id"]
        ) for card in cards_disponiveis
    ]
    
    response = client.get(f"/card/?ciclo_id={ciclo_id}")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert all(card["ciclo_id"] == ciclo_id for card in data)
    mock_get_cards_by_ciclo.assert_called_once()

# Testes de Obter Card por ID
@patch("service.card_service.CardService.get_card_by_id")
def test_obter_card_por_id(mock_get_card_by_id):
    card_disponivel = cards_fake(1)[0]
    mock_get_card_by_id.return_value = CardResponseDTO(
        id=card_disponivel["id"],
        status=card_disponivel["status"],
        tempo_planejado_horas=card_disponivel["tempo_planejado_horas"],
        link=card_disponivel["link"],
        descricao=card_disponivel["descricao"],
        ciclo_id=card_disponivel["ciclo_id"],
        fase_id=card_disponivel["fase_id"],
        artefato_id=card_disponivel["artefato_id"],
        responsavel_id=card_disponivel["responsavel_id"]
    )
    
    response = client.get(f"/card/{card_disponivel['id']}")
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == card_disponivel["id"]
    assert data["descricao"] == card_disponivel["descricao"]
    assert data["status"] == card_disponivel["status"]
    mock_get_card_by_id.assert_called_once()

@patch("service.card_service.CardService.get_card_by_id")
def test_obter_card_por_id_nao_encontrado(mock_get_card_by_id):
    mock_get_card_by_id.return_value = None
    card_id = str(uuid.uuid4())
    
    response = client.get(f"/card/{card_id}")

    assert response.status_code == 404
    assert "Card não encontrado" in response.json()["detail"]

# Testes de Atualizar Card
@patch("service.card_service.CardService.update_card")
def test_atualizar_card(mock_update_card, card_update):
    card_id = str(uuid.uuid4())
    card_atualizado = cards_fake(1)[0]
    card_atualizado["id"] = card_id
    card_atualizado["status"] = CardStatus.EM_ANDAMENTO
    card_atualizado["tempo_planejado_horas"] = 8.0
    card_atualizado["link"] = "http://exemplo.com/tarefa/123/atualizado"
    card_atualizado["descricao"] = "Implementar funcionalidade de teste com validações"
    
    mock_update_card.return_value = CardResponseDTO(
        id=card_atualizado["id"],
        status=card_atualizado["status"],
        tempo_planejado_horas=card_atualizado["tempo_planejado_horas"],
        link=card_atualizado["link"],
        descricao=card_atualizado["descricao"],
        ciclo_id=card_atualizado["ciclo_id"],
        fase_id=card_atualizado["fase_id"],
        artefato_id=card_atualizado["artefato_id"],
        responsavel_id=card_atualizado["responsavel_id"]
    )
    
    response = client.patch(f"/card/{card_id}", json=card_update.model_dump(exclude_unset=True))
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == card_id
    assert data["status"] == card_atualizado["status"]
    assert data["tempo_planejado_horas"] == card_atualizado["tempo_planejado_horas"]
    mock_update_card.assert_called_once()

@patch("service.card_service.CardService.update_card")
def test_atualizar_card_nao_encontrado(mock_update_card, card_update):
    mock_update_card.return_value = None
    card_id = str(uuid.uuid4())
    
    response = client.patch(f"/card/{card_id}", json=card_update.model_dump(exclude_unset=True))

    assert response.status_code == 404
    assert "Card não encontrado" in response.json()["detail"]

@patch("service.card_service.CardService.update_card")
def test_atualizar_card_erro_validacao(mock_update_card, card_update):
    mock_update_card.side_effect = ValueError("Fase não encontrada")
    card_id = str(uuid.uuid4())
    
    response = client.patch(f"/card/{card_id}", json=card_update.model_dump(exclude_unset=True))

    assert response.status_code == 400
    assert "Fase não encontrada" in response.json()["detail"]

# Testes de Deletar Card
@patch("service.card_service.CardService.delete_card")
def test_deletar_card(mock_delete_card):
    mock_delete_card.return_value = True
    card_id = str(uuid.uuid4())
    
    response = client.delete(f"/card/{card_id}")

    assert response.status_code == 204
    assert response.text == ''
    mock_delete_card.assert_called_once()

@patch("service.card_service.CardService.delete_card")
def test_deletar_card_nao_encontrado(mock_delete_card):
    mock_delete_card.return_value = False
    card_id = str(uuid.uuid4())
    
    response = client.delete(f"/card/{card_id}")

    assert response.status_code == 404
    assert "Card não encontrado" in response.json()["detail"]


# Testes de Serviço (Unit tests)
def test_criar_card_sucesso_service(mocker, card_create):
    fake_id = str(uuid.uuid4())
    fake_card_response = CardResponseDTO(
        id=fake_id,
        status=card_create.status,
        tempo_planejado_horas=card_create.tempo_planejado_horas,
        link=card_create.link,
        descricao=card_create.descricao,
        ciclo_id=card_create.ciclo_id,
        fase_id=card_create.fase_id,
        artefato_id=card_create.artefato_id,
        responsavel_id=card_create.responsavel_id
    )

    mock_create = mocker.patch.object(
        CardService,
        'create_card',
        return_value=fake_card_response
    )

    import asyncio
    result = asyncio.run(CardService.create_card(None, card_create))
    
    assert result.status == card_create.status
    assert result.tempo_planejado_horas == card_create.tempo_planejado_horas
    assert result.descricao == card_create.descricao
    assert hasattr(result, "id")

def test_criar_card_erro_validacao_service(mocker, card_create):
    mock_create = mocker.patch.object(
        CardService,
        'create_card',
        side_effect=ValueError("Ciclo não encontrado")
    )

    with pytest.raises(ValueError, match="Ciclo não encontrado"):
        import asyncio
        asyncio.run(CardService.create_card(None, card_create))

def test_listar_cards_service(mocker):
    cards_disponiveis = cards_fake(3)
    fake_cards_response = [
        CardResponseDTO(
            id=card["id"],
            status=card["status"],
            tempo_planejado_horas=card["tempo_planejado_horas"],
            link=card["link"],
            descricao=card["descricao"],
            ciclo_id=card["ciclo_id"],
            fase_id=card["fase_id"],
            artefato_id=card["artefato_id"],
            responsavel_id=card["responsavel_id"]
        ) for card in cards_disponiveis
    ]

    mock_get_all = mocker.patch.object(
        CardService,
        'get_all_cards',
        return_value=fake_cards_response
    )

    import asyncio
    result = asyncio.run(CardService.get_all_cards(None))
    
    assert len(result) == 3
    assert result[0].descricao == cards_disponiveis[0]["descricao"]

def test_obter_card_por_id_service(mocker):
    card_disponivel = cards_fake(1)[0]
    fake_card_response = CardResponseDTO(
        id=card_disponivel["id"],
        status=card_disponivel["status"],
        tempo_planejado_horas=card_disponivel["tempo_planejado_horas"],
        link=card_disponivel["link"],
        descricao=card_disponivel["descricao"],
        ciclo_id=card_disponivel["ciclo_id"],
        fase_id=card_disponivel["fase_id"],
        artefato_id=card_disponivel["artefato_id"],
        responsavel_id=card_disponivel["responsavel_id"]
    )

    mock_get_by_id = mocker.patch.object(
        CardService,
        'get_card_by_id',
        return_value=fake_card_response
    )

    import asyncio
    result = asyncio.run(CardService.get_card_by_id(None, card_disponivel["id"]))
    
    assert result is not None
    assert result.id == card_disponivel["id"]
    assert result.descricao == card_disponivel["descricao"]
