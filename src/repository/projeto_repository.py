from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from typing import Optional, List
from psycopg2.extras import RealDictRow
from datetime import datetime
import uuid

from utils.functions import print_error_details


async def get_all_projetos(conn: connection) -> List[RealDictRow]:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                SELECT id, nome, descritivo, created_at, updated_at
                FROM projeto
                ORDER BY created_at DESC;
            """)
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print_error_details(e)
            raise e


async def get_projeto_by_id(conn: connection, projeto_id: str) -> Optional[RealDictRow]:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                SELECT id, nome, descritivo, created_at, updated_at
                FROM projeto
                WHERE id = %s;
            """, (projeto_id,))
            projeto = cursor.fetchone()
            return projeto
        except Exception as e:
            print_error_details(e)
            raise e


async def projeto_name_exists(conn: connection, nome: str, exclude_id: Optional[str] = None) -> bool:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            if exclude_id:
                cursor.execute("""
                    SELECT COUNT(*) as count
                    FROM projeto
                    WHERE nome = %s AND id != %s;
                """, (nome, exclude_id))
            else:
                cursor.execute("""
                    SELECT COUNT(*) as count
                    FROM projeto
                    WHERE nome = %s;
                """, (nome,))

            result = cursor.fetchone()
            return result['count'] > 0
        except Exception as e:
            print_error_details(e)
            raise e


async def create_projeto(conn: connection, projeto_data: dict) -> Optional[RealDictRow]:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            
            now = datetime.utcnow()
            cursor.execute("""
                INSERT INTO projeto (nome, descritivo, created_at)
                VALUES (%s, %s, %s)
                RETURNING id, nome, descritivo, created_at;
            """, (projeto_data.get('nome'), projeto_data.get('descritivo'), now))

            created = cursor.fetchone()
            conn.commit()
            return created
        except Exception as e:
            conn.rollback()
            print_error_details(e)
            return None


async def update_projeto(conn: connection, projeto_id: str, projeto_data: dict) -> Optional[RealDictRow]:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            now = datetime.utcnow()
            cursor.execute("""
                UPDATE projeto
                SET nome = %s, descritivo = %s, updated_at = %s
                WHERE id = %s
                RETURNING id, nome, descritivo, updated_at;
            """, (projeto_data.get('nome'), projeto_data.get('descritivo'), now, projeto_id))

            updated = cursor.fetchone()
            conn.commit()
            return updated
        except Exception as e:
            conn.rollback()
            print_error_details(e)
            raise e


async def delete_projeto(conn: connection, projeto_id: str) -> Optional[RealDictRow]:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                DELETE FROM projeto
                WHERE id = %s
                RETURNING id, nome;
            """, (projeto_id,))

            deleted = cursor.fetchone()
            conn.commit()
            return deleted
        except Exception as e:
            conn.rollback()
            print_error_details(e)
            raise e
