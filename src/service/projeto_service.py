from typing import List, Optional
from psycopg2.extensions import connection
from repository import projeto_repository
from utils.functions import print_error_details


class ProjetoService:

    @staticmethod
    async def create_projeto(conn: connection, projeto_data: dict) -> Optional[dict]:
        """
        Cria um projeto e associa os responsáveis.
        """
        try:
            # Verifica nome duplicado
            if await projeto_repository.projeto_name_exists(conn, projeto_data.get("nome")):
                raise ValueError("Já existe um projeto com esse nome.")

            # Cria o projeto
            created = await projeto_repository.create_projeto(conn, projeto_data)
            if not created:
                raise ValueError("Falha ao criar o projeto.")

            projeto_id = created.get("id")

            # Associa responsáveis (se houver)
            for responsavel_id in projeto_data.get("responsaveis_id", []):
                await projeto_repository.add_usuario_projeto(conn, projeto_id, responsavel_id)

            # Retorna projeto completo com responsáveis e ciclos
            projeto_completo = await projeto_repository.get_projeto_by_id(conn, projeto_id)
            return projeto_completo

        except Exception as e:
            print_error_details(e)
            raise e

    # -------------------------------------------------------------

    @staticmethod
    async def get_all_projetos(conn: connection) -> List[dict]:
        """
        Retorna todos os projetos com responsáveis e ciclos.
        """
        try:
            return await projeto_repository.get_all_projetos(conn)
        except Exception as e:
            print_error_details(e)
            return []

    # -------------------------------------------------------------

    @staticmethod
    async def get_projeto_by_id(conn: connection, projeto_id: str) -> Optional[dict]:
        """
        Retorna um projeto específico com responsáveis e ciclos.
        """
        try:
            projeto = await projeto_repository.get_projeto_by_id(conn, projeto_id)
            if not projeto:
                raise ValueError("Projeto não encontrado.")
            return projeto
        except Exception as e:
            print_error_details(e)
            return None

    # -------------------------------------------------------------

    @staticmethod
    async def update_projeto(conn: connection, projeto_id: str, projeto_data: dict) -> Optional[dict]:
        """
        Atualiza os dados de um projeto e reatribui responsáveis (opcionalmente).
        """
        try:
            # Verifica se nome já existe em outro projeto
            if await projeto_repository.projeto_name_exists(conn, projeto_data.get("nome"), exclude_id=projeto_id):
                raise ValueError("Já existe um projeto com esse nome.")

            # Atualiza informações básicas
            updated = await projeto_repository.update_projeto(conn, projeto_id, projeto_data)
            if not updated:
                raise ValueError("Falha ao atualizar o projeto.")

            # Se houver lista de responsáveis, atualiza associações
            if "responsaveis_id" in projeto_data:
                # Remove todos os vínculos anteriores
                projeto_atual = await projeto_repository.get_projeto_by_id(conn, projeto_id)
                for r in projeto_atual.get("responsaveis_dto", []):
                    await projeto_repository.remove_usuario_projeto(conn, projeto_id, r.get("id"))

                # Adiciona os novos vínculos
                for responsavel_id in projeto_data["responsaveis_id"]:
                    await projeto_repository.add_usuario_projeto(conn, projeto_id, responsavel_id)

            # Retorna o projeto completo atualizado
            projeto_atualizado = await projeto_repository.get_projeto_by_id(conn, projeto_id)
            return projeto_atualizado

        except Exception as e:
            print_error_details(e)
            raise e

    # -------------------------------------------------------------

    @staticmethod
    async def delete_projeto(conn: connection, projeto_id: str) -> bool:
        """
        Deleta um projeto e seus vínculos com usuários.
        """
        try:
            # Remove vínculos de usuários primeiro
            projeto = await projeto_repository.get_projeto_by_id(conn, projeto_id)
            if projeto and projeto.get("responsaveis_dto"):
                for r in projeto["responsaveis_dto"]:
                    await projeto_repository.remove_usuario_projeto(conn, projeto_id, r["id"])

            # Deleta o projeto
            deleted = await projeto_repository.delete_projeto(conn, projeto_id)
            return deleted is not None

        except Exception as e:
            print_error_details(e)
            return False
