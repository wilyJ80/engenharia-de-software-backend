from model.fase import Fase, FaseBase, FaseResponse, FaseUpdate
from repository import fase_repository
from psycopg2.extensions import connection
from fastapi import HTTPException


class FaseService:

    @staticmethod
    async def create_fase(
        db,
        fase: FaseBase,
    ) -> Fase | None:
        inserted_fase = await fase_repository.create_fase(db, fase)

        return inserted_fase

    @staticmethod
    async def get_all_fases(db: connection) -> list[FaseResponse]:
        return await fase_repository.get_all_fases(db)

    @staticmethod
    async def get_fase_by_id(
        db: connection, 
        fase_id: str,
    ) -> FaseResponse | None:
        return await fase_repository.get_fase_by_id(db, fase_id)

    @staticmethod
    async def update_fase(
        db: connection, 
        fase_id: str, 
        fase: FaseUpdate
    ) -> FaseResponse | None:
        return await fase_repository.update_fase(db, fase_id, fase)

    @staticmethod
    async def delete_fase(
        db: connection, 
        fase_id: str
    ) -> FaseResponse | None:
        return await fase_repository.delete_fase(db, fase_id)