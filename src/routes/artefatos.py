from http.client import HTTPException
from fastapi import APIRouter, status, Depends
from src.model.artefato import Artefato, ArtefatoBase
from src.service import artefato_service

router = APIRouter(prefix="/artefatos", tags=['artefatos'])

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Artefato,
    summary="Cria um novo artefato",
)
async def create_artefato(
    artefato: ArtefatoBase,
   # db = Depends(get_db)
):
    created_artefato = await artefato_service.create_artefato(artefato)

    if not created_artefato:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar o artefato."
        )
    
    return created_artefato