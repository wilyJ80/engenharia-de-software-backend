from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from utils.functions import print_error_details
from model.fase import FaseBase
from psycopg2.extras import RealDictRow

# |=======| LISTANDO TODOS AS FASES |=======|
async def get_all_fases(conn: connection):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""
                    SELECT id, nome, descritivo, ordem, created_at, updated_at 
                    FROM fase;
                """)

        return cursor.fetchall()

# FIND BY ID

async def get_fase_by_id(conn: connection, fase_id: int):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                            SELECT id, nome, descritivo, ordem FROM fase WHERE id = %s;
                        """, (fase_id,))

            return cursor.fetchone()
        except Exception as e:
            print_error_details(e)


# |=======| POST
async def create_fase(conn: connection, fase: FaseBase):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                            INSERT INTO fase (nome, descritivo, ordem) VALUES (%s, %s, %s) RETURNING id, nome, descritivo, ordem;
                        """, (fase.nome, fase.descritivo, fase.ordem))
            
            return cursor.fetchone()
        except Exception as e:
            print_error_details(e)
# PUT
async def update_fase(conn: connection, fase_id: int, fase: FaseBase) -> RealDictRow | None:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                            UPDATE fase SET nome = %s, descritivo = %s, ordem = %s WHERE id = %s RETURNING id, nome, descritivo, ordem;
                        """, (fase.nome, fase.descritivo, fase.ordem, fase_id))
            
            return cursor.fetchone()
        except Exception as e:
            print_error_details(e)


# DELETE
async def delete_fase(conn: connection, fase_id: int) -> RealDictRow | None:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                            DELETE FROM fase WHERE id = %s;
                        """, (fase_id,))
            
            return cursor.fetchone()
        except Exception as e:
            print_error_details(e)