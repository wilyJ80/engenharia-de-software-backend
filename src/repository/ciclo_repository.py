from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from model.ciclo import Ciclo
from model.dto.ciclo_dto import CicloCreateDTO, CicloUpdateDTO
from utils.functions import print_error_details
from psycopg2.extras import RealDictRow
from typing import Optional, List
from datetime import datetime
import uuid


# |=======| LISTANDO TODOS OS CICLOS |=======|
async def get_all_ciclos(conn: connection) -> List[RealDictRow]:
    """Retorna todos os ciclos do banco de dados."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                SELECT id, nome, versao, projeto_id, created_at, updated_at 
                FROM ciclo 
                ORDER BY created_at DESC;
            """)
            ciclos = cursor.fetchall()
            return ciclos
        except Exception as e:
            print_error_details(e)
            raise e


# |=======| BUSCAR CICLO POR ID |=======|
async def get_ciclo_by_id(
    conn: connection,
    ciclo_id: str
) -> Optional[RealDictRow]:
    """Busca um ciclo pelo ID."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                SELECT id, nome, versao, projeto_id, created_at, updated_at 
                FROM ciclo 
                WHERE id = %s;
            """, (ciclo_id,))
            ciclo = cursor.fetchone()
            return ciclo
        except Exception as e:
            print_error_details(e)
            raise e


# |=======| BUSCAR CICLO POR NOME |=======|
async def get_ciclo_by_nome(
    conn: connection,
    nome: str
) -> Optional[RealDictRow]:
    """Busca um ciclo pelo nome."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                SELECT id, nome, versao, projeto_id, created_at, updated_at 
                FROM ciclo 
                WHERE nome = %s;
            """, (nome,))
            ciclo = cursor.fetchone()
            return ciclo
        except Exception as e:
            print_error_details(e)
            raise e


# |=======| VERIFICAR SE NOME JÁ EXISTE |=======|
async def nome_exists(
    conn: connection,
    nome: str,
    exclude_id: Optional[str] = None
) -> bool:
    """Verifica se um nome já existe no banco, opcionalmente excluindo um ID específico."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            if exclude_id:
                cursor.execute("""
                    SELECT COUNT(*) as count 
                    FROM ciclo 
                    WHERE nome = %s AND id != %s;
                """, (nome, exclude_id))
            else:
                cursor.execute("""
                    SELECT COUNT(*) as count 
                    FROM ciclo 
                    WHERE nome = %s;
                """, (nome,))
            
            result = cursor.fetchone()
            return result['count'] > 0
        except Exception as e:
            print_error_details(e)
            raise e


# |=======| CRIAR CICLO |=======|
async def create_ciclo(
    conn: connection,
    ciclo_data: CicloCreateDTO
) -> Optional[RealDictRow]:
    """Cria um novo ciclo no banco de dados."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            ciclo_id = str(uuid.uuid4())
            now = datetime.utcnow()
            
            cursor.execute("""
                INSERT INTO ciclo (id, nome, versao, projeto_id, created_at) 
                VALUES (%s, %s, %s, %s, %s) 
                RETURNING id, nome, versao, projeto_id, created_at;
            """, (ciclo_id, ciclo_data.nome, ciclo_data.versao, ciclo_data.projeto_id, now))
            
            created_ciclo = cursor.fetchone()
            conn.commit()
            return created_ciclo
        except Exception as e:
            conn.rollback()
            print_error_details(e)
            return None


# |=======| ATUALIZAR CICLO |=======|
async def update_ciclo(
    conn: connection,
    ciclo_id: str,
    ciclo_data: CicloUpdateDTO
) -> Optional[RealDictRow]:
    """Atualiza um ciclo existente."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            now = datetime.utcnow()
            
            cursor.execute("""
                UPDATE ciclo 
                SET nome = %s, versao = %s, projeto_id = %s, updated_at = %s 
                WHERE id = %s 
                RETURNING id, nome, versao, projeto_id, updated_at;
            """, (ciclo_data.nome, ciclo_data.versao, ciclo_data.projeto_id, now, ciclo_id))
            
            updated_ciclo = cursor.fetchone()
            conn.commit()
            return updated_ciclo
        except Exception as e:
            conn.rollback()
            print_error_details(e)
            raise e


# |=======| DELETAR CICLO |=======|
async def delete_ciclo(
    conn: connection,
    ciclo_id: str
) -> Optional[RealDictRow]:
    """Deleta um ciclo do banco de dados."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                DELETE FROM ciclo 
                WHERE id = %s
                RETURNING id, nome, versao;
            """, (ciclo_id,))
            
            deleted_ciclo = cursor.fetchone()
            conn.commit()
            return deleted_ciclo
        except Exception as e:
            conn.rollback()
            print_error_details(e)
            raise e


# |=======| BUSCAR CICLOS POR VERSÃO |=======|
async def get_ciclos_by_versao(
    conn: connection,
    versao: str
) -> List[RealDictRow]:
    """Busca ciclos por versão."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                SELECT id, nome, versao, projeto_id, created_at, updated_at 
                FROM ciclo 
                WHERE versao = %s
                ORDER BY created_at DESC;
            """, (versao,))
            ciclos = cursor.fetchall()
            return ciclos
        except Exception as e:
            print_error_details(e)
            raise e


# |=======| BUSCAR CICLOS POR PROJETO |=======|
async def get_ciclos_by_projeto(
    conn: connection,
    projeto_id: str
) -> List[RealDictRow]:
    """Busca ciclos por projeto."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                SELECT id, nome, versao, projeto_id, created_at, updated_at 
                FROM ciclo 
                WHERE projeto_id = %s
                ORDER BY created_at DESC;
            """, (projeto_id,))
            ciclos = cursor.fetchall()
            return ciclos
        except Exception as e:
            print_error_details(e)
            raise e