from pydantic import BaseModel, Field


class responsavel_dto(BaseModel):
    id  : str = Field(..., description="Identificador único do responsavel")
    nome: str = Field(..., description="Nome do responsável")
