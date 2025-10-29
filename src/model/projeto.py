from pydantic import BaseModel, Field

class ProjetoBase(BaseModel):
    id: str = Field(..., description="Identificador único do projeto")
    nome: str = Field(description="Nome do projeto", example="Projeto01")
    descritivo: str = Field(description="Descrição do projeto", example="Projeto de Enegenharia de Software")