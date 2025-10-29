from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection

# |=======| LISTANDO TODOS AS FASES |=======|
async def get_all_fases(conn: connection):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""
                        SELECT id, nome, descritivo, ordem FROM fase;
                    """)
        
        return cursor.fetchall()
