# src/model/card.py
import uuid
from uuid import UUID
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime, Text, Enum as SQLModelEnum
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from ._common import CardStatus # Importa o Enum

class Card(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid.uuid4, # Padrão para o Pydantic (na aplicação)
        sa_column=Column(
            PG_UUID(as_uuid=True),
            primary_key=True,
            server_default=func.gen_random_uuid(), # Padrão para o Postgres (no banco)
            nullable=False
        )
    )
    
    status: CardStatus = Field(
        sa_column=Column(SQLModelEnum(CardStatus), index=True, nullable=False), 
        default=CardStatus.a_fazer
    )
    tempo_planejado_horas: float = Field(nullable=False)
    link: Optional[str] = Field(default=None)
    descricao: Optional[str] = Field(default=None, sa_column=Column(Text))

    # Chaves Estrangeiras
    ciclo_id: UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), foreign_key="ciclo.id", nullable=False)
    )
    fase_id: UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), foreign_key="fase.id", nullable=False)
    )
    artefato_id: UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), foreign_key="artefato.id", nullable=False)
    )
    responsavel_id: UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), foreign_key="usuario.id", nullable=False)
    )

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
        default_factory=datetime.utcnow
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
        default_factory=datetime.utcnow
    )

    # Relacionamentos
    ciclo: "Ciclo" = Relationship(back_populates="cards")
    fase: "Fase" = Relationship(back_populates="cards")
    artefato: "Artefato" = Relationship(back_populates="cards")
    responsavel: "Usuario" = Relationship(back_populates="cards_responsaveis")