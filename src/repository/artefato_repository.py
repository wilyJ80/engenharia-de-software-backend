from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor

from src.model.artefato import ArtefatoBase

async def get_artefato_by_name(
    conn: connection,
    nome_artefato: str,
):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""
                        SELECT id, nome, created_at, updated_at FROM Artefato
                        WHERE nome = %s
                    """, (nome_artefato,))

        return cursor.fetchone()
    
async def create_artefato(
        conn: connection, 
        artefato: ArtefatoBase
):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""
                        INSERT INTO Artefato (nome) 
                       VALUES (%s)
                       RETURNING nome, id, created_at;
                """, (artefato.nome))

        created = cursor.fetchone()
        conn.commit()
        return created