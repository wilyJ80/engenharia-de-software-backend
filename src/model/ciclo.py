from pydantic import BaseModel, Field
from datetime import datetime

from .base import Base

class Ciclo(Base):
    id: str = Field(..., description="Identificador único do ciclo")
    nome: str = Field(..., description="Nome do ciclo")
    versao: str = Field(..., description="Versão do ciclo")
    projeto_id: str = Field(..., description="Identificador do projeto associado")