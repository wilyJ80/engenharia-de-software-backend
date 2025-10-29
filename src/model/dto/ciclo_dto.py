from pydantic import BaseModel, Field

class CicloCreateDTO(BaseModel):
    nome: str = Field(..., description="Nome do ciclo", example="Ciclo de Desenvolvimento")
    versao: str = Field(..., description="Versão do ciclo", example="1.0.0")
    projeto_id: str = Field(..., description="Identificador do projeto associado", example="550e8400-e29b-41d4-a716-446655440000")

class CicloUpdateDTO(BaseModel):
    nome: str = Field(..., description="Nome do ciclo", example="Ciclo de Desenvolvimento")
    versao: str = Field(..., description="Versão do ciclo", example="1.0.1")
    projeto_id: str = Field(..., description="Identificador do projeto associado", example="550e8400-e29b-41d4-a716-446655440000")

class CicloResponseDTO(BaseModel):
    id: str = Field(..., description="Identificador único do ciclo")
    nome: str = Field(..., description="Nome do ciclo")
    versao: str = Field(..., description="Versão do ciclo")
    projeto_id: str = Field(..., description="Identificador do projeto associado")