from pydantic import Field
from .card_status import CardStatus
from .base import Base

class CardModel(Base):
    status : CardStatus = Field(description="Status do card")
    tempo_planejado_horas : float = Field(description="Tempo de execução planejado para aquele card")
    link: str = Field(description="Link")
    descricao: str = Field(description="Descrição do card")
    ciclo_id: str = Field(..., description="Identificador do ciclo associado")
    fase_id: str = Field(..., description="Identificador da fase associado")
    artefato_id: str = Field(..., description="Identificador do artefato associado")
    responsavel_id: str = Field(..., description="Identificador do responsável associado")