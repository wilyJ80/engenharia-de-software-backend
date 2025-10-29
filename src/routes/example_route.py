from fastapi import APIRouter

from model.example import Example

router = APIRouter(prefix="/example", tags=['example'])

@router.get("/", response_model=Example)
async def get_exemplo():
    ex01 = Example(name = "Exemplo")
    return ex01