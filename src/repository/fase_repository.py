from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from utils.functions import print_error_details
from model.fase import FaseBase, FaseUpdate
from psycopg2.extras import RealDictRow
from psycopg2.extras import execute_values

# |=======| LISTANDO TODOS AS FASES |=======|
async def get_all_fases(
    conn: connection
) -> list[RealDictRow]:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                SELECT 
                    f.id, 
                    f.nome, 
                    f.descritivo,
                    f.ordem,
                    COALESCE(
                        JSON_AGG(
                            JSON_BUILD_OBJECT('id', a.id, 'nome', a.nome)
                        ) FILTER (WHERE a.id IS NOT NULL), 
                        '[]'::json
                    ) AS artefatos
                FROM 
                    fase AS f
                LEFT JOIN 
                    faseartefato AS fa ON f.id = fa.fase_id
                LEFT JOIN 
                    artefato AS a ON fa.artefato_id = a.id
                GROUP BY 
                    f.id
                ORDER BY
                    f.ordem;
            """)
            fases = cursor.fetchall()
            return fases
        except Exception as e:
            print_error_details(e)
            raise e

# FIND BY ID

async def get_fase_by_id(
        conn: connection, 
        fase_id: str
) -> RealDictRow | None:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                SELECT 
                    f.id, f.nome, f.descritivo, f.ordem,
                    COALESCE(
                        JSON_AGG(
                            JSON_BUILD_OBJECT('id', a.id, 'nome', a.nome)
                        ) FILTER (WHERE a.id IS NOT NULL),
                        '[]'::json
                    ) AS artefatos
                FROM 
                    fase AS f
                LEFT JOIN 
                    faseartefato AS fa ON f.id = fa.fase_id
                LEFT JOIN 
                    artefato AS a ON fa.artefato_id = a.id
                WHERE 
                    f.id = %s
                GROUP BY 
                    f.id;
            """, (fase_id,))
            return cursor.fetchone()
        except Exception as e:
            print_error_details(e)
            raise e


# |=======| POST
def create_fase(
    conn: connection, 
    fase: FaseBase
) -> RealDictRow | None:
    new_fase_id = None
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute(
                """
                INSERT INTO fase (nome, descritivo, ordem) 
                VALUES (%s, %s, %s) 
                RETURNING id;
                """,
                (fase.nome, fase.descritivo, fase.ordem)
            )
            new_fase_id = cursor.fetchone()['id']

            if fase.artefato_ids and len(fase.artefato_ids) > 0:

                associacoes_para_inserir = [
                    (new_fase_id, artefato_id) for artefato_id in fase.artefato_ids
                ]
                
                execute_values(
                    cursor,
                    "INSERT INTO faseartefato (fase_id, artefato_id) VALUES %s",
                    associacoes_para_inserir
                )

            conn.commit()

        except Exception as e:
            conn.rollback()
            print_error_details(e)
            raise e

    if new_fase_id:
        return get_fase_by_id(conn, new_fase_id)
    
    return None
# PUT
async def update_fase(
        conn: connection, 
        fase_id: int, fase: FaseUpdate
) -> RealDictRow | None:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute(
                """
                UPDATE fase 
                SET nome = %s, descritivo = %s, ordem = %s 
                WHERE id = %s 
                RETURNING id;
                """,
                (fase.nome, fase.descritivo, fase.ordem, fase_id)
            )
            if cursor.fetchone() is None:
                conn.rollback()
                return None

            cursor.execute("DELETE FROM faseartefato WHERE fase_id = %s", (fase_id,))

            if fase.artefato_ids:
                new_associations = [(fase_id, artefato_id) for artefato_id in fase.artefato_ids]
                execute_values(
                    cursor,
                    "INSERT INTO faseartefato (fase_id, artefato_id) VALUES %s",
                    new_associations
                )

            conn.commit()

        except Exception as e:
            conn.rollback()
            print_error_details(e)
            raise e

    return await get_fase_by_id(conn, fase_id)


# DELETE
async def delete_fase(conn: connection, fase_id: str) -> RealDictRow | None:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute(
                "DELETE FROM faseartefato WHERE fase_id = %s",
                (fase_id,)
            )
            cursor.execute(
                "DELETE FROM fase WHERE id = %s RETURNING id, nome",
                (fase_id,)
            )
            
            deleted_fase = cursor.fetchone()

            if deleted_fase is None:
                conn.rollback()
                return None

            conn.commit()

            # print(f'retorno da query -> {deleted_fase}')
            
            return deleted_fase

        except Exception as e:
            conn.rollback()
            print_error_details(e)
            raise e