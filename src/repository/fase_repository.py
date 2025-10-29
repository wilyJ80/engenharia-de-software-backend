from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from utils.functions import print_error_details

# |=======| LISTANDO TODOS AS FASES |=======|
async def get_all_fases(conn: connection):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""
                        SELECT id, nome, descritivo, ordem FROM fase;
                    """)

        return cursor.fetchall()

# FIND BY ID

async def get_fase_by_id(conn: connection, fase_id: int):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                            SELECT id, nome, descritivo, ordem FROM fase WHERE id = %s;
                        """)

            cursor.execute(cursor, (fase_id,))
            return cursor.fetchone()
        except Exception as e:
            print_error_details(e)


# |=======| POST

# PUT

# DELETE
