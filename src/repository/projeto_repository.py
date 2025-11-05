from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from typing import Optional, List, Dict, Any
from psycopg2.extras import RealDictRow
from datetime import datetime

from utils.functions import print_error_details


# 🔹 Buscar todos os projetos com responsáveis e ciclos resumidos
async def get_all_projetos(conn: connection) -> List[Dict[str, Any]]:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                SELECT 
                    p.id,
                    p.nome,
                    p.descritivo,
                    p.created_at,
                    p.updated_at,
                    COALESCE(
                        JSON_AGG(
                            DISTINCT JSONB_BUILD_OBJECT(
                                'id', u.id,
                                'nome', u.nome,
                                'email', u.email
                            )
                        ) FILTER (WHERE u.id IS NOT NULL), '[]'
                    ) AS responsaveis_dto,
                    COALESCE(
                        JSON_AGG(
                            DISTINCT JSONB_BUILD_OBJECT(
                                'id', c.id,
                                'nome', c.nome,
                                'versao', c.versao,
                                'created_at', c.created_at
                            )
                        ) FILTER (WHERE c.id IS NOT NULL), '[]'
                    ) AS ciclos_dto
                FROM projeto p
                LEFT JOIN projetousuario pu ON p.id = pu.projeto_id
                LEFT JOIN usuario u ON pu.usuario_id = u.id
                LEFT JOIN ciclo c ON c.projeto_id = p.id
                GROUP BY p.id
                ORDER BY p.created_at DESC;
            """)
            return cursor.fetchall()
        except Exception as e:
            print_error_details(e)
            raise e


# 🔹 Buscar um projeto por ID com responsáveis e ciclos
async def get_projeto_by_id(conn: connection, projeto_id: str) -> Optional[Dict[str, Any]]:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                SELECT 
                    p.id,
                    p.nome,
                    p.descritivo,
                    p.created_at,
                    p.updated_at,
                    COALESCE(
                        JSON_AGG(
                            DISTINCT JSONB_BUILD_OBJECT(
                                'id', u.id,
                                'nome', u.nome,
                                'email', u.email
                            )
                        ) FILTER (WHERE u.id IS NOT NULL), '[]'
                    ) AS responsaveis_dto,
                    COALESCE(
                        JSON_AGG(
                            DISTINCT JSONB_BUILD_OBJECT(
                                'id', c.id,
                                'nome', c.nome,
                                'versao', c.versao,
                                'created_at', c.created_at
                            )
                        ) FILTER (WHERE c.id IS NOT NULL), '[]'
                    ) AS ciclos_dto
                FROM projeto p
                LEFT JOIN projetousuario pu ON p.id = pu.projeto_id
                LEFT JOIN usuario u ON pu.usuario_id = u.id
                LEFT JOIN ciclo c ON c.projeto_id = p.id
                WHERE p.id = %s
                GROUP BY p.id;
            """, (projeto_id,))
            return cursor.fetchone()
        except Exception as e:
            print_error_details(e)
            raise e


# 🔹 Verificar se nome de projeto já existe (excluindo um ID opcional)
async def projeto_name_exists(conn: connection, nome: str, exclude_id: Optional[str] = None) -> bool:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            if exclude_id:
                cursor.execute("""
                    SELECT COUNT(*) AS count
                    FROM projeto
                    WHERE nome = %s AND id != %s;
                """, (nome, exclude_id))
            else:
                cursor.execute("""
                    SELECT COUNT(*) AS count
                    FROM projeto
                    WHERE nome = %s;
                """, (nome,))
            return cursor.fetchone()['count'] > 0
        except Exception as e:
            print_error_details(e)
            raise e


# 🔹 Criar novo projeto
async def create_projeto(conn: connection, projeto_data: dict) -> Optional[Dict[str, Any]]:
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


# 🔹 Atualizar projeto
async def update_projeto(conn: connection, projeto_id: str, projeto_data: dict) -> Optional[Dict[str, Any]]:
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


# 🔹 Deletar projeto
async def delete_projeto(conn: connection, projeto_id: str) -> Optional[Dict[str, Any]]:
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


# 🔹 Associar usuário a projeto
async def add_usuario_projeto(conn: connection, projeto_id: str, usuario_id: str):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                INSERT INTO projetousuario (projeto_id, usuario_id)
                VALUES (%s, %s)
                RETURNING projeto_id, usuario_id;
            """, (projeto_id, usuario_id))
            added = cursor.fetchone()
            conn.commit()
            return added
        except Exception as e:
            conn.rollback()
            print_error_details(e)
            raise e


# 🔹 Remover usuário de projeto
async def remove_usuario_projeto(conn: connection, projeto_id: str, usuario_id: str):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                DELETE FROM projetousuario
                WHERE projeto_id = %s AND usuario_id = %s
                RETURNING projeto_id, usuario_id;
            """, (projeto_id, usuario_id))
            removed = cursor.fetchone()
            conn.commit()
            return removed
        except Exception as e:
            conn.rollback()
            print_error_details(e)
            raise e
