from http.client import HTTPException
from fastapi import APIRouter, status, Depends, Request
from psycopg2.extensions import connection
from model.fase import FaseBase, Fase
from service.fase_service import FaseService
from db.database import get_db

fase_router = APIRouter(prefix="/api/v1", tags=['fase'])

@fase_router.post(
    "/create_fase",
    status_code=status.HTTP_201_CREATED,
    response_model=Fase,
    summary="Cria uma nova fase",
)
async def create_fase(
   request: FaseBase,
   db: connection = Depends(get_db),
):
    fase = await request.body()
    created_fase = await FaseService.create_fase(db, fase)

    if not created_fase:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar o artefato."
        )

    return created_fase

@fase_router.get("/get_all_fases", response_model=list[Fase])
async def get_all_fases(db: connection = Depends(get_db),):
    return await FaseService.get_all_fases(db)

@fase_router.get("/{fase_id}", response_model=Fase)
async def get_fase_by_id(fase_id: str, db: connection = Depends(get_db),):
    return await FaseService.get_fase_by_id(db, fase_id)

@fase_router.put("/{fase_id}", response_model=Fase)
async def update_fase(fase_id, fase:FaseBase, db: connection = Depends(get_db),):
    return await FaseService.update_fase(db, fase_id, fase)


@fase_router.delete("/{fase_id}", response_model=Fase)
async def delete_fase(fase_id, db: connection = Depends(get_db),):
    return await FaseService.delete_fase(db, fase_id)