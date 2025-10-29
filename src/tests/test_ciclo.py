import pytest
import uuid
import os
import sys

# Adiciona o diretório src ao sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from model.dto.ciclo_dto import CicloCreateDTO, CicloUpdateDTO, CicloResponseDTO

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
        versao="1.1.0",
        projeto_id=str(uuid.uuid4())
    )

def test_ciclo_create_dto():
    projeto_id = str(uuid.uuid4())
    ciclo = CicloCreateDTO(
        nome="Ciclo de Desenvolvimento",
        versao="2.0.0",
        projeto_id=projeto_id
    )
    assert ciclo.nome == "Ciclo de Desenvolvimento"
    assert ciclo.versao == "2.0.0"
    assert ciclo.projeto_id == projeto_id

def test_ciclo_create_dto_validation():
    # Testa se todos os campos são obrigatórios
    with pytest.raises(ValueError):
        CicloCreateDTO()
    
    with pytest.raises(ValueError):
        CicloCreateDTO(nome="Teste")
    
    with pytest.raises(ValueError):
        CicloCreateDTO(nome="Teste", versao="1.0.0")

def test_ciclo_update_dto():
    projeto_id = str(uuid.uuid4())
    ciclo = CicloUpdateDTO(
        nome="Ciclo Atualizado",
        versao="2.1.0",
        projeto_id=projeto_id
    )
    assert ciclo.nome == "Ciclo Atualizado"
    assert ciclo.versao == "2.1.0"
    assert ciclo.projeto_id == projeto_id

def test_ciclo_response_dto():
    ciclo_id = str(uuid.uuid4())
    projeto_id = str(uuid.uuid4())
    ciclo = CicloResponseDTO(
        id=ciclo_id,
        nome="Ciclo Response",
        versao="3.0.0",
        projeto_id=projeto_id
    )
    assert ciclo.id == ciclo_id
    assert ciclo.nome == "Ciclo Response"
    assert ciclo.versao == "3.0.0"
    assert ciclo.projeto_id == projeto_id

def test_ciclo_serialization():
    projeto_id = str(uuid.uuid4())
    ciclo = CicloCreateDTO(
        nome="Ciclo Serialização",
        versao="1.5.0",
        projeto_id=projeto_id
    )
    data = ciclo.model_dump()
    expected = {
        "nome": "Ciclo Serialização",
        "versao": "1.5.0",
        "projeto_id": projeto_id
    }
    assert data == expected

def test_ciclo_deserialization():
    projeto_id = str(uuid.uuid4())
    data = {
        "nome": "Ciclo Deserialização",
        "versao": "2.3.0",
        "projeto_id": projeto_id
    }
    ciclo = CicloCreateDTO(**data)
    assert ciclo.nome == "Ciclo Deserialização"
    assert ciclo.versao == "2.3.0"
    assert ciclo.projeto_id == projeto_id

def test_ciclo_update_vs_create_dto():
    projeto_id = str(uuid.uuid4())
    
    # Ambos devem ter os mesmos campos
    create_data = {
        "nome": "Teste Ciclo",
        "versao": "1.0.0",
        "projeto_id": projeto_id
    }
    
    ciclo_create = CicloCreateDTO(**create_data)
    ciclo_update = CicloUpdateDTO(**create_data)
    
    assert ciclo_create.nome == ciclo_update.nome
    assert ciclo_create.versao == ciclo_update.versao
    assert ciclo_create.projeto_id == ciclo_update.projeto_id

def test_ciclo_response_with_id():
    ciclo_id = str(uuid.uuid4())
    projeto_id = str(uuid.uuid4())
    
    # Response deve incluir o ID
    response_data = {
        "id": ciclo_id,
        "nome": "Ciclo com ID",
        "versao": "1.2.0",
        "projeto_id": projeto_id
    }
    
    ciclo_response = CicloResponseDTO(**response_data)
    assert hasattr(ciclo_response, "id")
    assert ciclo_response.id == ciclo_id