# src/model/fase.py
import uuid
from uuid import UUID
from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from .fase_artefato import FaseArtefato

class Fase(SQLModel, table=True):
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
    descritivo: str = Field(sa_column=Column(Text))
    ordem: int

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
        default_factory=datetime.utcnow
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
        default_factory=datetime.utcnow
    )

    # Relacionamentos
    artefatos: List["Artefato"] = Relationship(back_populates="fases", link_model=FaseArtefato)
    cards: List["Card"] = Relationship(back_populates="fase")