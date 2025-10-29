from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from model.usuario import Usuario
from model.dto.usuario_dto import UsuarioCreateDTO
from utils.functions import print_error_details
from psycopg2.extras import RealDictRow
from typing import Optional, List
from datetime import datetime
import uuid


# |=======| LISTANDO TODOS OS USUÁRIOS |=======|
async def get_all_usuarios(conn: connection) -> List[RealDictRow]:
    """Retorna todos os usuários do banco de dados."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                SELECT id, nome, email, created_at, updated_at 
                FROM usuario 
                ORDER BY created_at DESC;
            """)
            usuarios = cursor.fetchall()
            return usuarios
        except Exception as e:
            print_error_details(e)
            raise e


# |=======| BUSCAR USUÁRIO POR ID |=======|
async def get_usuario_by_id(
    conn: connection,
    usuario_id: str
) -> Optional[RealDictRow]:
    """Busca um usuário pelo ID."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                SELECT id, nome, email, created_at, updated_at 
                FROM usuario 
                WHERE id = %s;
            """, (usuario_id,))
            usuario = cursor.fetchone()
            return usuario
        except Exception as e:
            print_error_details(e)
            raise e


# |=======| BUSCAR USUÁRIO POR EMAIL |=======|
async def get_usuario_by_email(
    conn: connection,
    email: str
) -> Optional[RealDictRow]:
    """Busca um usuário pelo email."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                SELECT id, nome, email, senha_hash, created_at, updated_at 
                FROM usuario 
                WHERE email = %s;
            """, (email,))
            usuario = cursor.fetchone()
            return usuario
        except Exception as e:
            print_error_details(e)
            raise e


# |=======| VERIFICAR SE EMAIL JÁ EXISTE |=======|
async def email_exists(
    conn: connection,
    email: str,
    exclude_id: Optional[str] = None
) -> bool:
    """Verifica se um email já existe no banco, opcionalmente excluindo um ID específico."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            if exclude_id:
                cursor.execute("""
                    SELECT COUNT(*) as count 
                    FROM usuario 
                    WHERE email = %s AND id != %s;
                """, (email, exclude_id))
            else:
                cursor.execute("""
                    SELECT COUNT(*) as count 
                    FROM usuario 
                    WHERE email = %s;
                """, (email,))
            
            result = cursor.fetchone()
            return result['count'] > 0
        except Exception as e:
            print_error_details(e)
            raise e


# |=======| CRIAR USUÁRIO |=======|
async def create_usuario(
    conn: connection,
    usuario_data: UsuarioCreateDTO,
    senha_hash: str
) -> Optional[RealDictRow]:
    """Cria um novo usuário no banco de dados."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            user_id = str(uuid.uuid4())
            now = datetime.utcnow()
            
            cursor.execute("""
                INSERT INTO usuario (id, nome, email, senha_hash, created_at) 
                VALUES (%s, %s, %s, %s, %s) 
                RETURNING id, nome, email, created_at;
            """, (user_id, usuario_data.nome, usuario_data.email, senha_hash, now))
            
            created_user = cursor.fetchone()
            conn.commit()
            return created_user
        except Exception as e:
            conn.rollback()
            print_error_details(e)
            return None


# |=======| ATUALIZAR USUÁRIO |=======|
async def update_usuario(
    conn: connection,
    usuario_id: str,
    usuario_data: UsuarioCreateDTO,
    senha_hash: Optional[str] = None
) -> Optional[RealDictRow]:
    """Atualiza um usuário existente."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            now = datetime.utcnow()
            
            if senha_hash:
                cursor.execute("""
                    UPDATE usuario 
                    SET nome = %s, email = %s, senha_hash = %s, updated_at = %s 
                    WHERE id = %s 
                    RETURNING id, nome, email, updated_at;
                """, (usuario_data.nome, usuario_data.email, senha_hash, now, usuario_id))
            else:
                cursor.execute("""
                    UPDATE usuario 
                    SET nome = %s, email = %s, updated_at = %s 
                    WHERE id = %s 
                    RETURNING id, nome, email, updated_at;
                """, (usuario_data.nome, usuario_data.email, now, usuario_id))
            
            updated_user = cursor.fetchone()
            conn.commit()
            return updated_user
        except Exception as e:
            conn.rollback()
            print_error_details(e)
            raise e


# |=======| DELETAR USUÁRIO |=======|
async def delete_usuario(
    conn: connection,
    usuario_id: str
) -> Optional[RealDictRow]:
    """Deleta um usuário do banco de dados."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                DELETE FROM usuario 
                WHERE id = %s
                RETURNING id, nome, email;
            """, (usuario_id,))
            
            deleted_user = cursor.fetchone()
            conn.commit()
            return deleted_user
        except Exception as e:
            conn.rollback()
            print_error_details(e)
            raise e


# |=======| AUTENTICAR USUÁRIO |=======|
async def get_usuario_for_authentication(
    conn: connection,
    email: str
) -> Optional[RealDictRow]:
    """Busca um usuário para autenticação (inclui senha_hash)."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                SELECT id, nome, email, senha_hash, created_at, updated_at 
                FROM usuario 
                WHERE email = %s;
            """, (email,))
            usuario = cursor.fetchone()
            return usuario
        except Exception as e:
            print_error_details(e)
            raise e