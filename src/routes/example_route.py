from fastapi import APIRouter

from model.exemple import Example

router = APIRouter(prefix="/exemple", tags=['example'])

@router.get("/", response_model=Example)
async def get_exemplo():
    ex01 = Example(name = "Exemplo")
    return ex01