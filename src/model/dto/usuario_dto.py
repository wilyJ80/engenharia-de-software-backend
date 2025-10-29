from pydantic import Field, EmailStr

class UsuarioCreateDTO():
    senha: str = Field(default="123", description="Senha do usuário", example="123456", min_length=3)

class UsuarioLoginDTO():
    email: EmailStr = Field(description="Email do usuário", example="alan.victor@email.com")
    senha: str = Field(description="Senha do usuário", example="123456")

class UsuarioResponseDTO():
    id: str = Field(..., description="Identificador único do usuário")

