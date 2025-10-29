from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

from .base import Base

class Usuario(Base):

    id: str = Field(..., description="Identificador único do usuário")
    nome: str = Field(..., description="Nome do usuário")
    email: EmailStr = Field(..., description="Email do usuário")
    senha_hash: str = Field(..., description="Hash da senha do usuário")
