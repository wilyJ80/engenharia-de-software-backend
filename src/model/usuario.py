# src/model/usuario.py
import uuid
from uuid import UUID
from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime
from sqlalchemy.sql import func  # <--- CORRETO
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from .projeto_usuario import ProjetoUsuario

class Usuario(SQLModel, table=True):
    
    # --- INÍCIO DA CORREÇÃO ---
    id: UUID = Field(
        default_factory=uuid.uuid4, # Padrão para o Pydantic (na aplicação)
        sa_column=Column(
            PG_UUID(as_uuid=True),
            primary_key=True,
            server_default=func.gen_random_uuid(), # Padrão para o Postgres (no banco)
            nullable=False
        )
    )

    nome: str = Field(index=True)
    email: str = Field(unique=True, index=True, nullable=False)
    senha: str = Field(nullable=False)

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
        default_factory=datetime.utcnow
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
        default_factory=datetime.utcnow
    )

    # Relacionamentos
    projetos: List["Projeto"] = Relationship(back_populates="usuarios", link_model=ProjetoUsuario)
    cards_responsaveis: List["Card"] = Relationship(back_populates="responsavel")