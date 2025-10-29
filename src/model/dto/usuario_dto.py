from pydantic import BaseModel, Field, EmailStr

class UsuarioCreateDTO(BaseModel):
    nome: str = Field(..., description="Nome do usuário")
    email: EmailStr = Field(..., description="Email do usuário")

class UsuarioLoginDTO(BaseModel):
    email: EmailStr = Field(..., description="Email do usuário", example="alan.victor@email.com")
    senha: str = Field(..., description="Senha do usuário", example="123456")

class UsuarioResponseDTO(BaseModel):
    id: str = Field(..., description="Identificador único do usuário")
    nome: str = Field(..., description="Nome do usuário")
    email: EmailStr = Field(..., description="Email do usuário")

