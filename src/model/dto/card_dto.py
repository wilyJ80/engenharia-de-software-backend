from pydantic import BaseModel, Field
from model.card_status import CardStatus
from typing import Optional
from datetime import datetime

# DTO para Criação (CREATE)
class CardCreateDTO(BaseModel):
    status: CardStatus = Field(..., description="Status do card", example="PENDING")
    tempo_planejado_horas: float = Field(..., description="Tempo de execução planejado para aquele card", example=4.5)
    link: str = Field(..., description="Link associado ao card", example="http://exemplo.com/tarefa/123")
    descricao: str = Field(..., description="Descrição detalhada do card", example="Implementar a funcionalidade de login via OAuth.")
    ciclo_id: str = Field(..., description="Identificador do ciclo associado")
    fase_id: str = Field(..., description="Identificador da fase associado")
    artefato_id: str = Field(..., description="Identificador do artefato associado")
    responsavel_id: str = Field(..., description="Identificador do responsável associado")

class CardUpdateDTO(BaseModel):
    status: Optional[str] = Field(None, description="Status do card", example="IN_PROGRESS")
    tempo_planejado_horas: Optional[float] = Field(None, description="Tempo de execução planejado para aquele card", example=8.0)
    link: Optional[str] = Field(None, description="Link associado ao card", example="http://exemplo.com/tarefa/123/atualizado")
    descricao: Optional[str] = Field(None, description="Descrição detalhada do card", example="Implementar a funcionalidade de login via OAuth com testes.")
    fase_id: Optional[str] = Field(None, description="Identificador da fase associado")
    artefato_id: Optional[str] = Field(None, description="Identificador do artefato associado")
    responsavel_id: Optional[str] = Field(None, description="Identificador do responsável associado")

class CardResponseDTO(BaseModel):
    id: str = Field(..., description="Identificador único do card")
    status: CardStatus = Field(..., description="Status do card")
    tempo_planejado_horas: float = Field(..., description="Tempo de execução planejado para aquele card")
    link: str = Field(..., description="Link associado ao card")
    descricao: str = Field(..., description="Descrição do card")
    ciclo_id: str = Field(..., description="Identificador do ciclo associado")
    fase_id: str = Field(..., description="Identificador da fase associado")
    artefato_id: str = Field(..., description="Identificador do artefato associado")
    responsavel_id: str = Field(..., description="Identificador do responsável associado")
    created_at: datetime = Field(..., description="Data de criação do registro")
    updated_at: Optional[datetime] = Field(None, description="Data da última atualização do registro")