# src/model/projeto_usuario.py
import uuid
from uuid import UUID
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

class ProjetoUsuario(SQLModel, table=True):
    """Associação N:N entre Projetos e Usuários (Equipes)."""
    projeto_id: UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), foreign_key="projeto.id", primary_key=True)
    )
    usuario_id: UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), foreign_key="usuario.id", primary_key=True)
    )
    
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
        default_factory=datetime.utcnow
    )