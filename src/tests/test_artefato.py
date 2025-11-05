import pytest
import uuid
from datetime import datetime
import os
import sys

# Adiciona o diretório src ao sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from model.artefato import ArtefatoBase, Artefato, ArtefatoResponse

@pytest.fixture
def artefato_base():
    return ArtefatoBase(nome="Artefato de Teste")


def test_artefato_base_model():
    artefato = ArtefatoBase(nome="Teste de Artefato")
    assert artefato.nome == "Teste de Artefato"
    assert hasattr(artefato, "nome")


def test_artefato_base_validation():
    # Testa se o campo nome é obrigatório
    with pytest.raises(ValueError):
        ArtefatoBase()


def test_artefato_base_serialization():
    artefato = ArtefatoBase(nome="Teste de Serialização")
    data = artefato.model_dump()
    assert data == {"nome": "Teste de Serialização"}


def test_artefato_response_model():
    artefato_id = str(uuid.uuid4())
    artefato = ArtefatoResponse(
        id=artefato_id,
        nome="Artefato Response"
    )
    assert artefato.id == artefato_id
    assert artefato.nome == "Artefato Response"


def test_artefato_complete_model():
    artefato_id = str(uuid.uuid4())
    now = datetime.now()
    artefato = Artefato(
        id=artefato_id,
        nome="Artefato Completo",
        created_at=now,
        updated_at=now
    )
    assert artefato.id == artefato_id
    assert artefato.nome == "Artefato Completo"
    assert artefato.created_at == now
    assert artefato.updated_at == now


def test_artefato_inheritance():
    # Testa se ArtefatoResponse herda de ArtefatoBase
    artefato = ArtefatoResponse(id=str(uuid.uuid4()), nome="Teste")
    assert isinstance(artefato, ArtefatoBase)
    
    # Testa se Artefato herda de ArtefatoResponse
    artefato_full = Artefato(
        id=str(uuid.uuid4()),
        nome="Teste",
        created_at=datetime.now()
    )
    assert isinstance(artefato_full, ArtefatoResponse)
    assert isinstance(artefato_full, ArtefatoBase)

    #editar, apagar, rotas