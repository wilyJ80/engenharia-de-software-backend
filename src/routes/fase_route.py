from fastapi import APIRouter

from model.fase import FaseBase

router = APIRouter(prefix="/example", tags=['example'])

@router.get("/", response_model=FaseBase)
async def get_all_fases():
    return []

@router.get("/{fase_id}", response_model=FaseBase)
async def get_fase_byId(fase_id: str):
    return None

@router.post("/", response_model=FaseBase)
async def create_fase(fase: FaseBase):
    return None

@router.put("/", response_model=FaseBase)
async def edit_fase(fase: FaseBase):
    return None

@router.delete("/{fase_id}", response_model=FaseBase)
async def delete_fase(fase: FaseBase):
    return None