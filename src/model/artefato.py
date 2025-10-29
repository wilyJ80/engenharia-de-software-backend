from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ArtefatoBase(BaseModel):
    nome: str = Field(description="Nome do artefato", example="Artefato01")

class ArtefatoResponse(ArtefatoBase):
    id: str = Field(..., description="Identificador único da Revista")

class Artefato(ArtefatoResponse):
    created_at: datetime           = Field(..., description="Data de criação do registro")
    updated_at: Optional[datetime] = Field(None, description="Data da última atualização do registro")