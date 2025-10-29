from http.client import HTTPException
from fastapi import APIRouter, status, Depends, Request
from model.fase import FaseBase, Fase
from service.fase_service import FaseService

fase_router = APIRouter(prefix="/api/v1", tags=['fase'])

@fase_router.post(
    "/create_fase",
    status_code=status.HTTP_201_CREATED,
    response_model=Fase,
    summary="Cria uma nova fase",
)
async def create_fase(
   # db = Depends(get_db)
   request: Request
):
    fase = await request.body()
    created_fase = await FaseService.create_fase(fase)

    if not created_fase:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar o artefato."
        )

    return created_fase

@fase_router.get("/get_all_fases", response_model=list[Fase])
async def get_all_fases():
    return await FaseService.get_all_fases()

@fase_router.get("/get_fase_by_id", response_model=Fase)
async def get_fase_by_id(request: Request):
    fase_id = request.query_params.get("fase_id")
    return await FaseService.get_fase_by_id(fase_id)

@fase_router.put("/update_fase", response_model=Fase)
async def update_fase(request: Request):
    body = await request.body()
    fase_id = body.get('fase_id')
    fase = body.get('fase')
    return await FaseService.update_fase(fase_id, fase)


@fase_router.delete("/delete_fase", response_model=Fase)
async def delete_fase(request: Request):
    body = request.body()
    fase_id = body.get('fase_id')
    return await FaseService.delete_fase(fase_id)