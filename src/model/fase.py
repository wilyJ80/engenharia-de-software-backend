from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from model.artefato import ArtefatoResponse

class FaseBase(BaseModel):
    nome : str = Field(description="Nome da fase", example="Elaboração")
    descritivo: str = Field(description="Descrição da fase", example="Fase de elaboração do produto.")
    #artefato_ids: Optional[list[str]] = Field(None, description="Lista opcional de IDs de artefatos existentes para associar à nova fase.")
    ordem: int = Field(description="Ordem da fase", example=1)

class FaseCreate(BaseModel):
    nome : str = Field(description="Nome da fase", example="Elaboração")
    descritivo: str = Field(description="Descrição da fase", example="Fase de elaboração do produto.")
    artefato_ids: Optional[list[str]] = Field(None, description="Lista opcional de IDs de artefatos existentes para associar à nova fase.")
    ordem: int = Field(description="Ordem da fase", example=1)


class FaseResponse(FaseBase):
    id: str = Field(..., description="Identificador único da Fase")
    artefatos: Optional[list[ArtefatoResponse]] = Field(None, description="lista de artefatos", )

class Fase(FaseResponse):
    created_at: datetime           = Field(..., description="Data de criação do registro")
    updated_at: Optional[datetime] = Field(None, description="Data da última atualização do registro")
