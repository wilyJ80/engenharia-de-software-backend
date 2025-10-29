# src/model/fase_artefato.py
import uuid
from uuid import UUID
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

class FaseArtefato(SQLModel, table=True):
    """Associação N:N entre Fases e Artefatos (Configuração)."""
    fase_id: UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), foreign_key="fase.id", primary_key=True)
    )
    artefato_id: UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), foreign_key="artefato.id", primary_key=True)
    )
    
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
        default_factory=datetime.utcnow
    )