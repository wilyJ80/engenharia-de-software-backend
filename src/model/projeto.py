from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from .base import Base


class ProjetoBase(BaseModel):
    nome: str = Field(..., description="Nome do projeto", example="Projeto01")
    descritivo: Optional[str] = Field(None, description="Descrição do projeto", example="Projeto de Engenharia de Software")


class ProjetoResponse(ProjetoBase):
    id: str = Field(..., description="Identificador único do projeto")


class Projeto(ProjetoResponse):
    created_at: datetime = Field(..., description="Data de criação do registro")
    updated_at: Optional[datetime] = Field(None, description="Data da última atualização do registro")