import random
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional

from model.dto.card_dto import CardCreateDTO, CardResponseDTO, CardStatus, CardUpdateDTO
from service.card_service import CardService
from db.connection import Connection


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
@router.get(
    "/",
    response_model=List[CardResponseDTO],
    summary="Lista todos os Cards"
)
async def list_cards(
    # service: CardService = Depends(get_card_service),
    status_filtro: Optional[CardStatus] = Query(None, description="Filtra cards por Status"),
    ciclo_id: Optional[str] = Query(None, description="Filtra cards por ID do Ciclo associado")
):
    """
    Retorna uma lista de todos os Cards, com opções de filtragem por status ou ID do Ciclo.
    """
    # cards = service.list(status=status_filtro, ciclo_id=ciclo_id) # Chamada ao serviço
    # Simulação de dados:
    card_dummy = CardResponseDTO(
        id="a1b2c3d4-e5f6-7890-1234-567890abcdef",
        status=CardStatus.EM_ANDAMENTO,
        tempo_planejado_horas=10.0,
        link="http://exemplo.com/card_simulado",
        descricao="Card Simulado para listagem.",
        ciclo_id="c-id-123",
        fase_id="f-id-456",
        artefato_id="a-id-789",
        responsavel_id="r-id-012"
    )
    return [card_dummy]


# GET CARD ESPECÍFICO
@router.get(
    "/{card_id}",
    response_model=CardResponseDTO,
    summary="Obtém um Card específico pelo ID"
)
async def get_card(
    card_id: str,
    # service: CardService = Depends(get_card_service)
):
    """
    Retorna os detalhes de um Card específico.
    """
    # card = service.get_by_id(card_id) # Chamada ao serviço

    # Simulação:
    if card_id == "a1b2c3d4-e5f6-7890-1234-567890abcdef":
        return CardResponseDTO(
            id=card_id,
            status=CardStatus.A_FAZER,
            tempo_planejado_horas=5.0,
            link="http://exemplo.com/card_detalhe",
            descricao="Detalhes do Card solicitado.",
            ciclo_id="c-id-123",
            fase_id="f-id-456",
            artefato_id="a-id-789",
            responsavel_id="r-id-012"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Card com ID '{card_id}' não encontrado"
        )

# ATUALIZAR CARD
@router.patch(
    "/{card_id}",
    response_model=CardResponseDTO,
    summary="Atualiza um Card existente"
)
async def update_card(
    card_id: str,
    card_data: CardUpdateDTO,
    # service: CardService = Depends(get_card_service)
):
    """
    Atualiza um Card existente, permitindo a modificação de um subconjunto de campos.
    """
    # card_atualizado = service.update(card_id, card_data) # Chamada ao serviço

    # Simulação:
    if card_id != "a1b2c3d4-e5f6-7890-1234-567890abcdef":
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Card com ID '{card_id}' não encontrado para atualização"
        )

    # Simulação de merge dos dados
    dados_atuais = {
        "id": card_id,
        "status": CardStatus.A_FAZER,
        "tempo_planejado_horas": 5.0,
        "link": "http://exemplo.com/card_detalhe",
        "descricao": "Detalhes do Card solicitado.",
        "ciclo_id": "c-id-123",
        "fase_id": "f-id-456",
        "artefato_id": "a-id-789",
        "responsavel_id": "r-id-012"
    }

    # Atualiza apenas os campos que foram fornecidos
    campos_atualizaveis = card_data.model_dump(exclude_unset=True, exclude_none=True)
    dados_atuais.update(campos_atualizaveis)

    return CardResponseDTO(**dados_atuais)

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
    # sucesso = service.delete(card_id) # Chamada ao serviço
    # Simulação:
    if card_id == "card_inexistente":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Card com ID '{card_id}' não encontrado para exclusão"
        )
    # Retorna 204 No Content se a exclusão for bem-sucedida
    return