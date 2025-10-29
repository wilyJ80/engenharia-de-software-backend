from pydantic import BaseModel, Field

from .base import Base

class ProjetoBase(Base):
    id: str = Field(..., description="Identificador único do projeto")
    nome: str = Field(description="Nome do projeto", example="Projeto01")
    descritivo: str = Field(description="Descrição do projeto", example="Projeto de Enegenharia de Software")