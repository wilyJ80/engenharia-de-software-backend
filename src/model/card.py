from pydantic import Field, BaseModel
from datetime import datetime

from .card_status import CardStatus
from .base import Base

class CardModel(Base):
    id: str = Field(..., description="Identificador único do card")
    status : CardStatus = Field(description="Status do card")
    tempo_planejado_horas : float = Field(description="Tempo de execução planejado para aquele card")
    link: str = Field(description="Link")
    descricao: str = Field(description="Descrição do card")
    ciclo_id: str = Field(..., description="Identificador do ciclo associado")
    fase_id: str = Field(..., description="Identificador da fase associado")
    artefato_id: str = Field(..., description="Identificador do artefato associado")
    responsavel_id: str = Field(..., description="Identificador do responsável associado")
    started: datetime = Field(description="Data de início do andamento do card", default=None)
    progress: datetime = Field(description="Progresso do andamento das atividades do card", default=None)

class StatusModel(BaseModel):
    status: str = Field(description="Status do card")
    tempo_planejado_horas : float = Field(description="Tempo de execução planejado para aquele card")
