import pytest
import os
import sys

# Adiciona o diretório src ao sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from model.example import Example

def test_exemplo_model():
    example = Example(name="Teste")
    assert example.name == "Teste"
    assert hasattr(example, "name")

def test_exemplo_model_validation():
    # Testa se o campo name é obrigatório
    with pytest.raises(ValueError):
        Example()

def test_exemplo_model_serialization():
    example = Example(name="Teste de Serialização")
    data = example.model_dump()
    assert data == {"name": "Teste de Serialização"}

def test_exemplo_model_deserialization():
    data = {"name": "Teste de Deserialização"}
    example = Example(**data)
    assert example.name == "Teste de Deserialização"
