from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from utils.functions import print_error_details
from model.projeto import ProjetoBase  # Assumindo que este é o modelo para criação/update
from psycopg2.extras import RealDictRow
from typing import List

# |=======| CRIAR PROJETO |=======|
async def create_projeto(
    conn: connection,
    projeto: ProjetoBase
) -> RealDictRow | None:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                INSERT INTO projeto (nome, descritivo) 
                VALUES (%s, %s) 
                RETURNING id, nome, descritivo, created_at, updated_at;
            """, (projeto.nome, projeto.descritivo))
            
            created = cursor.fetchone()
            conn.commit()
            return created
        except Exception as e:
            conn.rollback()
            print_error_details(e)
            return None

# |=======| LISTAR TODOS OS PROJETOS |=======|
async def get_all_projetos(
    conn: connection
) -> List[RealDictRow]:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                SELECT id, nome, descritivo, created_at, updated_at 
                FROM projeto;
            """)
            return cursor.fetchall()
        except Exception as e:
            print_error_details(e)
            raise e

# |=======| BUSCAR PROJETO POR ID |=======|
async def get_projeto_by_id(
    conn: connection,
    projeto_id: str
) -> RealDictRow | None:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                SELECT id, nome, descritivo, created_at, updated_at 
                FROM projeto WHERE id = %s;
            """, (projeto_id,))
            
            return cursor.fetchone()
        except Exception as e:
            print_error_details(e)
            raise e

# |=======| ATUALIZAR PROJETO |=======|
async def update_projeto(
    conn: connection,
    projeto_id: str,
    projeto: ProjetoBase
) -> RealDictRow | None:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                UPDATE projeto 
                SET nome = %s, descritivo = %s, updated_at = NOW() 
                WHERE id = %s 
                RETURNING id, nome, descritivo, created_at, updated_at;
            """, (projeto.nome, projeto.descritivo, projeto_id))
            
            updated = cursor.fetchone()
            conn.commit()
            return updated
        except Exception as e:
            conn.rollback()
            print_error_details(e)
            raise e

# |=======| DELETAR PROJETO |=======|
async def delete_projeto(conn: connection, projeto_id: str) -> RealDictRow | None:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            # É importante deletar primeiro da tabela 'projetousuario'
            # para evitar erros de chave estrangeira.
            cursor.execute("""
                DELETE FROM projetousuario WHERE projeto_id = %s;
            """, (projeto_id,))
            
            # (Adicionar delete da tabela 'ciclo' aqui quando ela existir)

            # Agora deleta o projeto
            cursor.execute("""
                DELETE FROM projeto WHERE id = %s
                RETURNING id, nome;
            """, (projeto_id,))
            
            deleted = cursor.fetchone()
            conn.commit()
            return deleted
        except Exception as e:
            conn.rollback()
            print_error_details(e)
            raise e

# |=======| FUNÇÕES DE RELACIONAMENTO (PROJETO <-> USUARIO) |=======|

async def add_usuario_to_projeto(
    conn: connection,
    projeto_id: str,
    usuario_id: str
) -> RealDictRow | None:
    """ Adiciona um usuário a um projeto na tabela 'projetousuario' """
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                INSERT INTO projetousuario (projeto_id, usuario_id) 
                VALUES (%s, %s)
                RETURNING projeto_id, usuario_id, created_at;
            """, (projeto_id, usuario_id))
            
            created = cursor.fetchone()
            conn.commit()
            return created
        except Exception as e:
            conn.rollback()
            print_error_details(e)
            return None

async def get_usuarios_for_projeto(
    conn: connection,
    projeto_id: str
) -> List[RealDictRow]:
    """ Busca todos os usuários associados a um único projeto """
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                SELECT u.id, u.nome, u.email, u.created_at, u.updated_at 
                FROM usuario u
                JOIN projetousuario pu ON u.id = pu.usuario_id
                WHERE pu.projeto_id = %s;
            """, (projeto_id,))
            
            return cursor.fetchall()
        except Exception as e:
            print_error_details(e)
            raise e