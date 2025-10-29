from http.client import HTTPException
from fastapi import APIRouter, status, Depends
from src.model.artefato import Artefato, ArtefatoBase, ArtefatoResponse
from src.service import artefato_service
from psycopg2.extensions import connection
from src.db.database import get_db

router = APIRouter(prefix="/artefatos", tags=['artefatos'])

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Artefato,
    summary="Cria um novo artefato",
)
async def create_artefato(
    artefato: ArtefatoBase,
    db: connection = Depends(get_db),
):
    created_artefato = await artefato_service.create_artefato(db, artefato)

    if not created_artefato:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar o artefato."
        )
    
    return created_artefato

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[ArtefatoResponse],
    summary="Lista todos os artefatos",
)
async def get_all_artefatos(
    db: connection = Depends(get_db),
):
    artefatos = await artefato_service.get_all_artefatos(db)

    if not artefatos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum artefato encontrado."
        )
    
    return artefatos

@router.get(
    "/{artefato_id}",
    response_model=ArtefatoResponse,
    summary="Busca um artefato pelo ID",
)
async def get_artefato_by_id(
    artefato_id: str,
    db: connection = Depends(get_db),
):
    artefato = await artefato_service.get_artefato_by_id(db, artefato_id)
    if artefato is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Artefato com ID {artefato_id} não encontrado."
        )
    
    return artefato

@router.delete(
    "/{artefato_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta um artefato pelo ID",
)
async def delete_artefato(
    artefato_id: str,
    db: connection = Depends(get_db),
):
    deleted_artefato = await artefato_service.delete_artefato(db, artefato_id)
    if deleted_artefato is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Artefato com ID {artefato_id} não encontrado."
        )
    
    return

@router.put(
    "/{artefato_id}",
    status_code=status.HTTP_200_OK,
    response_model=ArtefatoResponse,
    summary="Atualiza um artefato pelo ID",
)
async def update_artefato(
    artefato_id: str,
    artefato: ArtefatoBase,
    db: connection = Depends(get_db),
):
    updated_artefato = await artefato_service.update_artefato(db, artefato_id, artefato)

    if not updated_artefato:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Já existe um artefato com o nome {artefato.nome}."
        )
    
    return updated_artefato