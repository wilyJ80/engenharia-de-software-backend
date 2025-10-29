from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from model.artefato import Artefato

class FaseBase(BaseModel):
    nome : str = Field(description="Nome da fase", example="")
    descritivo: str = Field(description="Descrição da fase", example="")
    artefato: Optional[list[Artefato]] = Field(None, description="Artefatos", example="")
    ordem: int = Field(description="Ordem da fase", example="")

class FaseResponse(FaseBase):
    id: str = Field(..., description="Identificador único da Fase")

class Fase(FaseResponse):
    created_at: datetime           = Field(..., description="Data de criação do registro")
    updated_at: Optional[datetime] = Field(None, description="Data da última atualização do registro")
