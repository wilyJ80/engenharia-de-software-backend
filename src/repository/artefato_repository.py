from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
#from psycopg2 import AsyncConnection
from model import artefato
from utils.functions import print_error_details
from model.artefato import ArtefatoBase
from psycopg2.extras import RealDictRow


# |=======| LISTANDO TODOS OS ARTEFATOS |=======|
async def get_all_artefatos(
        conn: connection
) -> list[RealDictRow]:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                            SELECT id, nome FROM artefato;
                        """)

            artefatos = cursor.fetchall()
            return artefatos
        except Exception as e:
            print_error_details(e)
            raise e

# FIND BY ID

async def get_artefato_by_id(
    conn: connection,
    artefato_id: str
) -> RealDictRow | None:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                            SELECT id, nome FROM artefato WHERE id = %s;
                        """, (artefato_id,))

            artefato = cursor.fetchone()
            return artefato
        except Exception as e:
            print_error_details(e)
            raise e


# |=======| POST
async def create_artefato(
    conn: connection,
    artefato: ArtefatoBase
) -> RealDictRow | None:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                            INSERT INTO artefato (nome) 
                            VALUES (%s) 
                            RETURNING id, nome, created_at;
                        """, (artefato.nome,))
            
            created = cursor.fetchone()
            conn.commit()
            return created
        except Exception as e:
            conn.rollback()
            print_error_details(e)
            return None

# PUT
async def update_artefato(
    conn: connection,
    artefato_id: str,
    artefato: ArtefatoBase
) -> RealDictRow | None:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                            UPDATE artefato SET nome = %s WHERE id = %s RETURNING id, nome;
                        """, (artefato.nome, artefato_id))
            updated = cursor.fetchone()
            conn.commit()
            return updated
        except Exception as e:
            conn.rollback()
            print_error_details(e)
            raise e

# DELETE
async def delete_artefato(conn: connection, artefato_id: str) -> RealDictRow | None:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                            DELETE FROM artefato WHERE id = %s
                            RETURNING id, nome;
                        """, (artefato_id,))
            deleted = cursor.fetchone()
            conn.commit()
            return deleted
        except Exception as e:
            conn.rollback()
            print_error_details(e)
            raise e


async def get_artefato_by_name(
    conn: connection,
    nome_artefato: str,
) -> RealDictRow | None:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                            SELECT id, nome, created_at, updated_at FROM artefato
                            WHERE nome = %s
                        """, (nome_artefato,))

            artefato = cursor.fetchone()
            return artefato
        except Exception as e:
            print_error_details(e)
            raise e