import stat
from fastapi import APIRouter, status, Depends, Request, HTTPException
from psycopg2.extensions import connection
from model.fase import FaseBase, Fase, FaseCreate, FaseResponse
from service.fase_service import FaseService
from db.database import get_db

fase_router = APIRouter(prefix="/fases", tags=['fase'])

@fase_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=FaseResponse,
    summary="Cria uma nova fase",
)
async def create_fase(
   fase: FaseCreate,
   db: connection = Depends(get_db),
):
    created_fase = await FaseService.create_fase(db, fase)

    if not created_fase:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar a fase."
        )

    return created_fase

@fase_router.get(
        "/", 
        response_model=list[FaseResponse],
        status_code=status.HTTP_200_OK,
        summary="Lista todas as fases",
)
async def get_all_fases(
    db: connection = Depends(get_db)
):
    fases = await FaseService.get_all_fases(db)
    if not fases:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Nenhuma fase encontrada."
        )
    
    return fases

@fase_router.get(
    "/{fase_id}", 
    response_model=FaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Busca uma fase pelo ID",
)
async def get_fase_by_id(fase_id: str, db: connection = Depends(get_db)):
    fase = await FaseService.get_fase_by_id(db, fase_id)
    if fase is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Fase com ID {fase_id} não encontrada."
        )
    return fase

@fase_router.put(
    "/{fase_id}", 
    response_model=FaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualiza uma fase pelo ID",
)
async def update_fase(
    fase_id: int, 
    fase: FaseBase, 
    db: connection = Depends(get_db)
):
    updated_fase = await FaseService.update_fase(db, fase_id, fase)

    if updated_fase is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Fase com ID {fase_id} não encontrada para atualização."
        )
    
    return updated_fase


@fase_router.delete(
    "/{fase_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta uma fase pelo ID",
)
async def delete_fase(
    fase_id: str, 
    db: connection = Depends(get_db)
):
    deleted_fase = await FaseService.delete_fase(db, fase_id)
    print(f'retorno -> {deleted_fase}')
    if deleted_fase is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Fase com ID {fase_id} não encontrada para deleção."
        )

    return