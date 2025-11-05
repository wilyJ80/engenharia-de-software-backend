import pytest
import uuid
from datetime import datetime
import os
import sys

# Adiciona o diretório src ao sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from model.projeto import ProjetoBase, Projeto, ProjetoResponse

@pytest.fixture
def projeto_base():
    return ProjetoBase(
        nome="Projeto de Teste",
        descritivo="Descrição do projeto de teste"
    )

def test_projeto_base_model():
    projeto = ProjetoBase(
        nome="Teste de Projeto",
        descritivo="Descrição detalhada"
    )
    assert projeto.nome == "Teste de Projeto"
    assert projeto.descritivo == "Descrição detalhada"
    assert hasattr(projeto, "nome")
    assert hasattr(projeto, "descritivo")

def test_projeto_base_validation():
    # Testa se o campo nome é obrigatório
    with pytest.raises(ValueError):
        ProjetoBase()
    
    # Descritivo é opcional
    projeto = ProjetoBase(nome="Projeto Sem Descrição")
    assert projeto.nome == "Projeto Sem Descrição"
    assert projeto.descritivo is None

def test_projeto_base_serialization():
    projeto = ProjetoBase(
        nome="Projeto Serialização",
        descritivo="Teste de serialização"
    )
    data = projeto.model_dump()
    expected = {
        "nome": "Projeto Serialização",
        "descritivo": "Teste de serialização"
    }
    assert data == expected


def test_projeto_response_model():
    projeto_id = str(uuid.uuid4())
    projeto = ProjetoResponse(
        id=projeto_id,
        nome="Projeto Response",
        descritivo="Projeto para response"
    )
    assert projeto.id == projeto_id
    assert projeto.nome == "Projeto Response"
    assert projeto.descritivo == "Projeto para response"
 

def test_projeto_complete_model():
    projeto_id = str(uuid.uuid4())
    now = datetime.now()
    projeto = Projeto(
        id=projeto_id,
        nome="Projeto Completo",
        descritivo="Projeto com timestamps",
        created_at=now,
        updated_at=now
    )
    assert projeto.id == projeto_id
    assert projeto.nome == "Projeto Completo"
    assert projeto.descritivo == "Projeto com timestamps"
    assert projeto.created_at == now
    assert projeto.updated_at == now


def test_projeto_inheritance():
    # Testa se ProjetoResponse herda de ProjetoBase
    projeto = ProjetoResponse(
        id=str(uuid.uuid4()),
        nome="Teste Herança",
        descritivo="Teste"
    )
    assert isinstance(projeto, ProjetoBase)
    
    # Testa se Projeto herda de ProjetoResponse
    projeto_full = Projeto(
        id=str(uuid.uuid4()),
        nome="Teste Herança Completa",
        descritivo="Teste completo",
        created_at=datetime.now()
    )
    assert isinstance(projeto_full, ProjetoResponse)
    assert isinstance(projeto_full, ProjetoBase)


def test_projeto_deserialization():
    projeto_id = str(uuid.uuid4())
    data = {
        "id": projeto_id,
        "nome": "Projeto Deserialização",
        "descritivo": "Teste de deserialização"
    }
    projeto = ProjetoResponse(**data)
    assert projeto.id == projeto_id
    assert projeto.nome == "Projeto Deserialização"
    assert projeto.descritivo == "Teste de deserialização"


def test_projeto_optional_fields():
    # Testa campos opcionais
    projeto = ProjetoBase(nome="Projeto Mínimo")
    assert projeto.nome == "Projeto Mínimo"
    assert projeto.descritivo is None
    
    # updated_at é opcional no modelo Projeto
    projeto_id = str(uuid.uuid4())
    now = datetime.now()
    projeto_completo = Projeto(
        id=projeto_id,
        nome="Projeto Timestamps",
        created_at=now
    )
    assert projeto_completo.updated_at is None
    assert projeto_completo.created_at == now