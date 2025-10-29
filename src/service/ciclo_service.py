from datetime import datetime
from typing import Optional, List
from psycopg2.extensions import connection
from model.ciclo import Ciclo
from model.dto.ciclo_dto import CicloCreateDTO, CicloUpdateDTO, CicloResponseDTO
from repository import ciclo_repository
from utils.functions import print_error_details

class CicloService:
    
    @staticmethod
    async def create_ciclo(conn: connection, ciclo_data: CicloCreateDTO) -> CicloResponseDTO:
        """Cria um novo ciclo."""
        try:
            # Verifica se o nome já existe
            if await ciclo_repository.nome_exists(conn, ciclo_data.nome):
                raise ValueError("Nome do ciclo já existe")
            
            # Cria o ciclo no banco
            created_ciclo = await ciclo_repository.create_ciclo(conn, ciclo_data)
            
            if not created_ciclo:
                raise ValueError("Erro ao criar ciclo")
            
            # Retorna resposta
            return CicloResponseDTO(
                id=created_ciclo['id'],
                nome=created_ciclo['nome'],
                versao=created_ciclo['versao'],
                projeto_id=created_ciclo['projeto_id']
            )
        except Exception as e:
            print_error_details(e)
            raise e
    
    @staticmethod
    async def get_ciclo_by_id(conn: connection, ciclo_id: str) -> Optional[CicloResponseDTO]:
        """Obtém um ciclo pelo ID."""
        try:
            ciclo_data = await ciclo_repository.get_ciclo_by_id(conn, ciclo_id)
            if ciclo_data:
                return CicloResponseDTO(
                    id=ciclo_data['id'],
                    nome=ciclo_data['nome'],
                    versao=ciclo_data['versao'],
                    projeto_id=ciclo_data['projeto_id']
                )
            return None
        except Exception as e:
            print_error_details(e)
            return None
    
    @staticmethod
    async def get_all_ciclos(conn: connection) -> List[CicloResponseDTO]:
        """Obtém todos os ciclos."""
        try:
            ciclos_data = await ciclo_repository.get_all_ciclos(conn)
            return [
                CicloResponseDTO(
                    id=ciclo['id'],
                    nome=ciclo['nome'],
                    versao=ciclo['versao'],
                    projeto_id=ciclo['projeto_id']
                )
                for ciclo in ciclos_data
            ]
        except Exception as e:
            print_error_details(e)
            return []
    
    @staticmethod
    async def update_ciclo(conn: connection, ciclo_id: str, ciclo_data: CicloUpdateDTO) -> Optional[CicloResponseDTO]:
        """Atualiza um ciclo."""
        try:
            # Verifica se o ciclo existe
            existing_ciclo = await ciclo_repository.get_ciclo_by_id(conn, ciclo_id)
            if not existing_ciclo:
                return None
            
            # Verifica se o novo nome já existe (exceto para o próprio ciclo)
            if await ciclo_repository.nome_exists(conn, ciclo_data.nome, ciclo_id):
                raise ValueError("Nome do ciclo já existe")
            
            # Atualiza o ciclo
            updated_ciclo = await ciclo_repository.update_ciclo(conn, ciclo_id, ciclo_data)
            
            if updated_ciclo:
                return CicloResponseDTO(
                    id=updated_ciclo['id'],
                    nome=updated_ciclo['nome'],
                    versao=updated_ciclo['versao'],
                    projeto_id=updated_ciclo['projeto_id']
                )
            return None
        except Exception as e:
            print_error_details(e)
            raise e
    
    @staticmethod
    async def delete_ciclo(conn: connection, ciclo_id: str) -> bool:
        """Deleta um ciclo."""
        try:
            deleted_ciclo = await ciclo_repository.delete_ciclo(conn, ciclo_id)
            return deleted_ciclo is not None
        except Exception as e:
            print_error_details(e)
            return False
    
    @staticmethod
    async def get_ciclo_by_nome(conn: connection, nome: str) -> Optional[CicloResponseDTO]:
        """Obtém um ciclo pelo nome."""
        try:
            ciclo_data = await ciclo_repository.get_ciclo_by_nome(conn, nome)
            if ciclo_data:
                return CicloResponseDTO(
                    id=ciclo_data['id'],
                    nome=ciclo_data['nome'],
                    versao=ciclo_data['versao'],
                    projeto_id=ciclo_data['projeto_id']
                )
            return None
        except Exception as e:
            print_error_details(e)
            return None
    
    @staticmethod
    async def get_ciclos_by_versao(conn: connection, versao: str) -> List[CicloResponseDTO]:
        """Obtém ciclos por versão."""
        try:
            ciclos_data = await ciclo_repository.get_ciclos_by_versao(conn, versao)
            return [
                CicloResponseDTO(
                    id=ciclo['id'],
                    nome=ciclo['nome'],
                    versao=ciclo['versao'],
                    projeto_id=ciclo['projeto_id']
                )
                for ciclo in ciclos_data
            ]
        except Exception as e:
            print_error_details(e)
            return []
    
    @staticmethod
    async def get_ciclos_by_projeto(conn: connection, projeto_id: str) -> List[CicloResponseDTO]:
        """Obtém ciclos por projeto."""
        try:
            ciclos_data = await ciclo_repository.get_ciclos_by_projeto(conn, projeto_id)
            return [
                CicloResponseDTO(
                    id=ciclo['id'],
                    nome=ciclo['nome'],
                    versao=ciclo['versao'],
                    projeto_id=ciclo['projeto_id']
                )
                for ciclo in ciclos_data
            ]
        except Exception as e:
            print_error_details(e)
            return []