from model.fase import Fase, FaseBase, FaseResponse
from repository import fase_repository
from fastapi import HTTPException


class FaseService:

    @staticmethod
    async def create_fase(
        #db,
        fase: FaseBase,
    ):

        existing_fase = await fase_repository.get_fase_by_id(fase.id)
        if existing_fase:
            return None

        inserted_fase = await fase_repository.create_fase(fase)

        return inserted_fase

    @staticmethod
    async def get_all_fases():
        fases = await fase_repository.get_all_fases()
        return fases

    @staticmethod
    async def get_fase_by_id(fase_id: int):
        if not fase_id:
            raise HTTPException(status_code=404, detail="fase_id is required")

        fase = await fase_repository.get_fase_by_id(fase_id)
        return fase

    @staticmethod
    async def update_fase(fase_id: int, fase: FaseBase):
        if not fase_id:
            raise HTTPException(status_code=404, detail="fase_id is required")

        if not fase:
            raise HTTPException(status_code=404, detail="fase is required")

        updated_fase = await fase_repository.update_fase(fase_id, fase)
        return updated_fase

    @staticmethod
    async def delete_fase(fase_id: int):
        if not fase_id:
            raise HTTPException(status_code=404, detail="fase_id is required")

        deleted_fase = await fase_repository.delete_fase(fase_id)
        return deleted_fase