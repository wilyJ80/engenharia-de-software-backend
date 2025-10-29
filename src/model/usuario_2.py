from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class Usuario(BaseModel):
    senha_hash: str = Field(..., description="Hash da senha do usuário")
    created_at: datetime = Field(..., description="Data de criação do registro")
    updated_at: Optional[datetime] = Field(None, description="Data da última atualização do registro")

class UsuarioBase(BaseModel):
    nome: str = Field(description="Nome do usuário", example="Alan Victor")
    email: EmailStr = Field(description="Email do usuário", example="alan.victor@email.com")

class UsuarioCreate(UsuarioBase):
    senha: str = Field(default="123", description="Senha do usuário", example="123456", min_length=3)

class UsuarioLogin(BaseModel):
    email: EmailStr = Field(description="Email do usuário", example="alan.victor@email.com")
    senha: str = Field(description="Senha do usuário", example="123456")

class UsuarioResponse(UsuarioBase):
    id: str = Field(..., description="Identificador único do usuário")

# class Usuario(UsuarioResponse):
#     senha_hash: str = Field(..., description="Hash da senha do usuário")
#     created_at: datetime = Field(..., description="Data de criação do registro")
#     updated_at: Optional[datetime] = Field(None, description="Data da última atualização do registro")

class Token(BaseModel):
    access_token: str = Field(..., description="Token de acesso JWT")
    token_type: str = Field(default="bearer", description="Tipo do token")

class TokenData(BaseModel):
    user_id: Optional[str] = None
