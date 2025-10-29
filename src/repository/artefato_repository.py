from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from utils.functions import print_error_details
from model.artefato import ArtefatoBase
from psycopg2.extras import RealDictRow


# |=======| LISTANDO TODOS OS ARTEFATOS |=======|
async def get_all_artefatos(conn: connection) -> list[RealDictRow]:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""
                        SELECT id, nome, descritivo, ordem FROM artefato;
                    """)

        return cursor.fetchall()

# FIND BY ID

async def get_artefato_by_id(
    conn: connection,
    artefato_id: int
) -> RealDictRow | None:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                            SELECT id, nome, descritivo, ordem FROM artefato WHERE id = %s;
                        """)

            cursor.execute(cursor, (artefato_id,))
            return cursor.fetchone()
        except Exception as e:
            print_error_details(e)


# |=======| POST
async def create_artefato(
    conn: connection,
    artefato: ArtefatoBase
) -> RealDictRow | None:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                            INSERT INTO artefato (nome) VALUES (%s) RETURNING id, nome;
                        """)
            cursor.execute(cursor, (artefato.nome,))
            return cursor.fetchone()
        except Exception as e:
            print_error_details(e)
# PUT
async def update_artefato(
    conn: connection,
    artefato_id: int,
    artefato: ArtefatoBase
) -> RealDictRow | None:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                            UPDATE artefato SET nome = %s WHERE id = %s RETURNING id, nome;
                        """)
            cursor.execute(cursor, (artefato.nome,))
            return cursor.fetchone()
        except Exception as e:
            print_error_details(e)


# DELETE
async def delete_artefato(conn: connection, artefato_id: int) -> RealDictRow | None:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                            DELETE FROM artefato WHERE id = %s;
                        """)
            cursor.execute(cursor, (artefato_id,))
            return cursor.fetchone()
        except Exception as e:
            print_error_details(e)