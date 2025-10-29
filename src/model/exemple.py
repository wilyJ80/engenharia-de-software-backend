from pydantic import BaseModel, Field

class Example(BaseModel):
    name: str = Field(..., description="Exemplo")