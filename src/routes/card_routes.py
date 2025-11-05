import random
import traceback
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional

from model.dto.card_dto import CardCreateDTO, CardResponseDTO, CardStatus, CardUpdateDTO
from service.card_service import CardService
from db.connection import Connection
from model.card import StatusModel


router = APIRouter(prefix="/card", tags=["card"])

# TODO: colocar a autenticação

# CRIAR NOVO CARD
@router.post(
    "/",
    response_model=CardResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo Card"
)
async def create_card(
    card_data: CardCreateDTO,
):
    """
    Cria um novo Card no sistema com todos os dados obrigatórios associados (ciclo, fase, artefato e responsável).
    """
    conn_instance = Connection()
    conn = conn_instance.get_conn()
    
    try:
        result = await CardService.create_card(conn, card_data)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
    finally:
        conn_instance.release_conn(conn)

# LISTAR TODOS OS CARDS (ou filtrar)
# TODO: verificar os filtros do get card
@router.get(
    "/",
    response_model=List,
    summary="Lista todos os Cards"
)
async def list_cards(
    status_filtro: Optional[CardStatus] = Query(None, description="Filtra cards por Status"),
    ciclo_id: Optional[str] = Query(None, description="Filtra cards por ID do Ciclo associado")
):
    """
    Retorna uma lista de todos os Cards, com opções de filtragem por status ou ID do Ciclo.
    """
    conn_instance = Connection()
    conn = conn_instance.get_conn()
    
    try:
        if status_filtro:
            cards = await CardService.get_cards_by_status(conn, status_filtro)
        elif ciclo_id:
            cards = await CardService.get_cards_by_ciclo(conn, ciclo_id)
        else:
            cards = await CardService.get_all_cards(conn)
        return cards
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
    finally:
        conn_instance.release_conn(conn)


# GET CARD ESPECÍFICO
@router.get(
    "/{card_id}",
    response_model=CardResponseDTO,
    summary="Obtém um Card específico pelo ID"
)
async def get_card(
    card_id: str,
):
    """
    Retorna os detalhes de um Card específico por id.
    """

    conn_instance = Connection()
    conn = conn_instance.get_conn()
    
    try:
        card = await CardService.get_card_by_id(conn, card_id)
        if not card:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Card não encontrado"
            )
        return card
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
    finally:
        conn_instance.release_conn(conn)

# ATUALIZAR CARD
@router.patch(
    "/{card_id}",
    response_model=CardResponseDTO,
    summary="Atualiza um Card existente"
)
async def update_card(
    card_id: str,
    card_data: CardUpdateDTO,
):
    """
    Atualiza um Card existente, permitindo a modificação de um subconjunto de campos.
    """
    # card_atualizado = service.update(card_id, card_data) # Chamada ao serviço

    conn_instance = Connection()
    conn = conn_instance.get_conn()
    
    try:
        update_card = await CardService.update_card(conn, card_id, card_data)
        if not update_card:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Card não encontrado"
            )
        return update_card
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
    finally:
        conn_instance.release_conn(conn)

# DELETAR CARD
@router.delete(
    "/{card_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta um Card pelo ID"
)
async def delete_card(
    card_id: str,
    # service: CardService = Depends(get_card_service)
):
    """
    Deleta permanentemente um Card do sistema.
    """
    conn_instance = Connection()
    conn = conn_instance.get_conn()
    
    try:
        deleted = await CardService.delete_card(conn, card_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Card não encontrado"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
    finally:
        conn_instance.release_conn(conn)


@router.patch("/alterarStatus/{card_id}")
async def patch_alterar_status(card_id: str, status: StatusModel):
    conn_instance = Connection()
    conn = conn_instance.get_conn()
    try:
        updated_card = await CardService.alterar_status(conn, card_id, status)
        return {"message": "Status atualizado com sucesso", "card": updated_card}
    finally:
        conn.close()