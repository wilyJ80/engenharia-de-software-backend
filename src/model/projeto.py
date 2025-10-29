from pydantic import BaseModel, Field
from model.usuario import Usuario

from .base import Base

class ProjetoBase(Base):
    id: str = Field(..., description="Identificador único do projeto")
    nome: str = Field(description="Nome do projeto", example="Projeto01")
    descritivo: str = Field(description="Descrição do projeto", example="Projeto de Enegenharia de Software")
    usuario: Usuario = Field()