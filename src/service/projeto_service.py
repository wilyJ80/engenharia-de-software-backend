from typing import List, Optional
from psycopg2.extensions import connection
from model.projeto import ProjetoResponse
from repository import projeto_repository
from utils.functions import print_error_details


class ProjetoService:

    @staticmethod
    async def create_projeto(conn: connection, projeto_data: dict) -> Optional[dict]:
        try:
            # verifica nome existente
            if await projeto_repository.projeto_name_exists(conn, projeto_data.get('nome')):
                raise ValueError("Já existe um projeto com esse nome")

            created = await projeto_repository.create_projeto(conn, projeto_data)
            if not created:
                return None

            return created
        except Exception as e:
            print_error_details(e)
            raise e

    @staticmethod
    async def get_all_projetos(conn: connection) -> List[dict]:
        try:
            rows = await projeto_repository.get_all_projetos(conn)
            return rows
        except Exception as e:
            print_error_details(e)
            return []

    @staticmethod
    async def get_projeto_by_id(conn: connection, projeto_id: str) -> Optional[dict]:
        try:
            projeto = await projeto_repository.get_projeto_by_id(conn, projeto_id)
            return projeto
        except Exception as e:
            print_error_details(e)
            return None

    @staticmethod
    async def update_projeto(conn: connection, projeto_id: str, projeto_data: dict) -> Optional[dict]:
        try:
            # verifica se nome já existe excluindo o próprio projeto
            if await projeto_repository.projeto_name_exists(conn, projeto_data.get('nome'), exclude_id=projeto_id):
                raise ValueError("Já existe um projeto com esse nome")

            updated = await projeto_repository.update_projeto(conn, projeto_id, projeto_data)
            return updated
        except Exception as e:
            print_error_details(e)
            raise e

    @staticmethod
    async def delete_projeto(conn: connection, projeto_id: str) -> bool:
        try:
            deleted = await projeto_repository.delete_projeto(conn, projeto_id)
            return deleted is not None
        except Exception as e:
            print_error_details(e)
            return False
