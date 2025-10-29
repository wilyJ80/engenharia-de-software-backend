from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Base(BaseModel):
    created_at: datetime = Field(..., description="Data de criação do registro")
    updated_at: Optional[datetime] = Field(None, description="Data da última atualização do registro")