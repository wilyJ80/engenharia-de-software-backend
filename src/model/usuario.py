from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    nome : str = Field(description="Nome do usuário", example="Alan Victor")
    email: str = Field(description="email do usuário", example="Alan Victor@email.com")
    senha: str = Field(description="senha do usuário", example="123")

class UsuarioResponse(UsuarioBase):
    id: str = Field(..., description="Identificador único da Revista")

class Usuario(UsuarioResponse):
    created_at: datetime           = Field(..., description="Data de criação do registro")
    updated_at: Optional[datetime] = Field(None, description="Data da última atualização do registro")
