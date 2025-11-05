from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from model.card import CardModel # Importação do seu modelo (usado apenas para tipagem no service)
from model.dto.card_dto import CardCreateDTO, CardUpdateDTO
from utils.functions import print_error_details
from psycopg2.extras import RealDictRow
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


# Os campos do CardModel são:
# status, tempo_planejado_horas, link, descricao, ciclo_id, fase_id, artefato_id, responsavel_id

CARD_COLUMNS = "id, status, tempo_planejado_horas, link, descricao, ciclo_id, fase_id, artefato_id, responsavel_id, created_at, updated_at"


# |=======| LISTANDO TODOS OS CARDS |=======|
async def get_all_cards(conn: connection) -> List[RealDictRow]:
    """Retorna todos os cards do banco de dados."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute(f"""
                SELECT {CARD_COLUMNS}
                FROM card
                ORDER BY created_at DESC;
            """)
            cards = cursor.fetchall()
            return cards
        except Exception as e:
            print_error_details(e)
            raise e


# |=======| BUSCAR CARD POR ID |=======|
async def get_card_by_id(
    conn: connection,
    card_id: str
) -> Optional[RealDictRow]:
    """Busca um card pelo ID."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute(f"""
                SELECT {CARD_COLUMNS}
                FROM card
                WHERE id = %s;
            """, (card_id,))
            card = cursor.fetchone()
            return card
        except Exception as e:
            print_error_details(e)
            raise e


# |=======| CRIAR CARD |=======|
async def create_card(
    conn: connection,
    card_data: CardCreateDTO
) -> Optional[RealDictRow]:
    """Cria um novo card no banco de dados."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            card_id = str(uuid.uuid4())
            now = datetime.utcnow()

            cursor.execute("""
                INSERT INTO card (
                    id, status, tempo_planejado_horas, link, descricao, 
                    ciclo_id, fase_id, artefato_id, responsavel_id, created_at
                ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                RETURNING id, status, tempo_planejado_horas, link, descricao, ciclo_id, fase_id, artefato_id, responsavel_id, created_at;
            """, (
                card_id,
                card_data.status.value, # Usamos .value para persistir o Enum como string
                card_data.tempo_planejado_horas, 
                card_data.link, 
                card_data.descricao, 
                card_data.ciclo_id, 
                card_data.fase_id, 
                card_data.artefato_id, 
                card_data.responsavel_id, 
                now
            ))

            created_card = cursor.fetchone()
            conn.commit()
            return created_card
        except Exception as e:
            conn.rollback()
            print_error_details(e)
            return None


# |=======| ATUALIZAR CARD (PATCH) |=======|
async def update_card(
    conn: connection,
    card_id: str,
    update_data: Dict[str, Any] # Espera um dicionário com os campos a serem atualizados
) -> Optional[RealDictRow]:
    """Atualiza um card existente. Realiza uma atualização parcial (PATCH)."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            now = datetime.utcnow()
            
            # 1. Cria a query de forma dinâmica
            set_clauses = []
            values = []
            
            # Mapeamento do Enum para string antes de construir a query
            if 'status' in update_data and update_data['status'] is not None:
                update_data['status'] = update_data['status']

            for key, value in update_data.items():
                # A chave 'id' é ignorada, se presente
                if key != 'id':
                    set_clauses.append(f"{key} = %s")
                    values.append(value)
            
            # Adiciona updated_at e o card_id no final
            set_clauses.append("updated_at = %s")
            values.append(now)
            values.append(card_id)

            set_clause = ", ".join(set_clauses)

            if not set_clause:
                return await get_card_by_id(conn, card_id) # Nada para atualizar

            query = f"""
                UPDATE card 
                SET {set_clause}
                WHERE id = %s 
                RETURNING {CARD_COLUMNS};
            """
            
            cursor.execute(query, tuple(values))

            updated_card = cursor.fetchone()
            conn.commit()
            return updated_card
        except Exception as e:
            conn.rollback()
            print_error_details(e)
            raise e


# |=======| DELETAR CARD |=======|
async def delete_card(
    conn: connection,
    card_id: str
) -> int: # Retorna o número de linhas afetadas (0 ou 1)
    """Deleta um card do banco de dados."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute("""
                DELETE FROM card 
                WHERE id = %s;
            """, (card_id,))
            
            deleted_count = cursor.rowcount
            conn.commit()
            return deleted_count
        except Exception as e:
            conn.rollback()
            print_error_details(e)
            raise e


# |=======| BUSCAR CARDS POR STATUS |=======|
async def get_cards_by_status(
    conn: connection,
    status: str
) -> List[RealDictRow]:
    """Busca cards por status."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute(f"""
                SELECT {CARD_COLUMNS}
                FROM card 
                WHERE status = %s
                ORDER BY created_at DESC;
            """, (status,))
            cards = cursor.fetchall()
            return cards
        except Exception as e:
            print_error_details(e)
            raise e


# |=======| BUSCAR CARDS POR CICLO |=======|
async def get_cards_by_ciclo(
    conn: connection,
    ciclo_id: str
) -> List[RealDictRow]:
    """Busca cards por ID do ciclo associado."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute(f"""
                SELECT {CARD_COLUMNS}
                FROM card 
                WHERE ciclo_id = %s
                ORDER BY created_at DESC;
            """, (ciclo_id,))
            cards = cursor.fetchall()
            return cards
        except Exception as e:
            print_error_details(e)
            raise e

# |=======| BUSCAR CARDS POR RESPONSÁVEL |=======|
async def get_cards_by_responsavel(
    conn: connection,
    responsavel_id: str
) -> List[RealDictRow]:
    """Busca cards por ID do responsável associado."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute(f"""
                SELECT {CARD_COLUMNS}
                FROM card 
                WHERE responsavel_id = %s
                ORDER BY created_at DESC;
            """, (responsavel_id,))
            cards = cursor.fetchall()
            return cards
        except Exception as e:
            print_error_details(e)
            raise e
        
# TODO: get card by fase; get card by projeto