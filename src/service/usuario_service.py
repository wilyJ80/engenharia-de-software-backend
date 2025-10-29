from datetime import datetime
from typing import Optional, List
from psycopg2.extensions import connection
from model.usuario import Usuario
from model.dto.usuario_dto import UsuarioCreateDTO, UsuarioResponseDTO
# Hash removido - usando senhas em texto plano
from repository import usuario_repository
from utils.functions import print_error_details

class UsuarioService:
    
    @staticmethod
    async def create_user(conn: connection, usuario_data: UsuarioCreateDTO) -> UsuarioResponseDTO:
        """Cria um novo usuário."""
        try:
            # Verifica se o email já existe
            if await usuario_repository.email_exists(conn, usuario_data.email):
                raise ValueError("Email já cadastrado")
            
            # Senha fixa para todos os usuários
            senha = "123"
            
            # Cria o usuário no banco
            created_user = await usuario_repository.create_usuario(conn, usuario_data, senha)
            
            if not created_user:
                raise ValueError("Erro ao criar usuário")
            
            # Retorna resposta sem a senha
            return UsuarioResponseDTO(
                id=created_user['id'],
                nome=created_user['nome'],
                email=created_user['email']
            )
        except Exception as e:
            print_error_details(e)
            raise e
    
    @staticmethod
    async def authenticate_user(conn: connection, email: str, senha: str) -> Optional[Usuario]:
        """Autentica um usuário."""
        try:
            user_data = await usuario_repository.get_usuario_for_authentication(conn, email)
            if user_data and senha == user_data['senha']:  # Comparação direta de senha
                return Usuario(
                    id=user_data['id'],
                    nome=user_data['nome'],
                    email=user_data['email'],
                    senha=user_data['senha'],
                    created_at=user_data['created_at'],
                    updated_at=user_data['updated_at']
                )
            return None
        except Exception as e:
            print_error_details(e)
            return None
    
    @staticmethod
    async def get_user_by_id(conn: connection, user_id: str) -> Optional[UsuarioResponseDTO]:
        """Obtém um usuário pelo ID."""
        try:
            user_data = await usuario_repository.get_usuario_by_id(conn, user_id)
            if user_data:
                return UsuarioResponseDTO(
                    id=user_data['id'],
                    nome=user_data['nome'],
                    email=user_data['email']
                )
            return None
        except Exception as e:
            print_error_details(e)
            return None
    
    @staticmethod
    async def get_all_users(conn: connection) -> List[UsuarioResponseDTO]:
        """Obtém todos os usuários."""
        try:
            users_data = await usuario_repository.get_all_usuarios(conn)
            return [
                UsuarioResponseDTO(
                    id=user['id'],
                    nome=user['nome'],
                    email=user['email']
                )
                for user in users_data
            ]
        except Exception as e:
            print_error_details(e)
            return []
    
    @staticmethod
    async def update_user(conn: connection, user_id: str, usuario_data: UsuarioCreateDTO) -> Optional[UsuarioResponseDTO]:
        """Atualiza um usuário."""
        try:
            # Verifica se o usuário existe
            existing_user = await usuario_repository.get_usuario_by_id(conn, user_id)
            if not existing_user:
                return None
            
            # Verifica se o novo email já existe (exceto para o próprio usuário)
            if await usuario_repository.email_exists(conn, usuario_data.email, user_id):
                raise ValueError("Email já cadastrado")
            
            # Senha fixa para todos os usuários
            senha = "123"
            
            # Atualiza o usuário
            updated_user = await usuario_repository.update_usuario(conn, user_id, usuario_data, senha)
            
            if updated_user:
                return UsuarioResponseDTO(
                    id=updated_user['id'],
                    nome=updated_user['nome'],
                    email=updated_user['email']
                )
            return None
        except Exception as e:
            print_error_details(e)
            raise e
    
    @staticmethod
    async def delete_user(conn: connection, user_id: str) -> bool:
        """Deleta um usuário."""
        try:
            deleted_user = await usuario_repository.delete_usuario(conn, user_id)
            return deleted_user is not None
        except Exception as e:
            print_error_details(e)
            return False
    
    @staticmethod
    async def get_user_by_email(conn: connection, email: str) -> Optional[UsuarioResponseDTO]:
        """Obtém um usuário pelo email."""
        try:
            user_data = await usuario_repository.get_usuario_by_email(conn, email)
            if user_data:
                return UsuarioResponseDTO(
                    id=user_data['id'],
                    nome=user_data['nome'],
                    email=user_data['email']
                )
            return None
        except Exception as e:
            print_error_details(e)
            return None