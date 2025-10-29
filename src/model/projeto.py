# src/model/projeto.py
import uuid
from uuid import UUID
from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from .projeto_usuario import ProjetoUsuario

class Projeto(SQLModel, table=True):
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

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
        default_factory=datetime.utcnow
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
        default_factory=datetime.utcnow
    )

    # Relacionamentos
    usuarios: List["Usuario"] = Relationship(back_populates="projetos", link_model=ProjetoUsuario)
    ciclos: List["Ciclo"] = Relationship(back_populates="projeto")