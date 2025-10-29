from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from model.dto.ciclo_dto import CicloCreateDTO, CicloUpdateDTO, CicloResponseDTO
from service.ciclo_service import CicloService
from core.auth import get_current_user
from db.connection import Connection

router = APIRouter(prefix="/ciclos", tags=["ciclos"])

@router.post("/", response_model=CicloResponseDTO, status_code=status.HTTP_201_CREATED)
async def criar_ciclo(
    ciclo: CicloCreateDTO,
    current_user_id: str = Depends(get_current_user)
):
    """Cria um novo ciclo."""
    conn_instance = Connection()
    conn = conn_instance.get_conn()
    
    try:
        result = await CicloService.create_ciclo(conn, ciclo)
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

@router.get("/", response_model=List[CicloResponseDTO])
async def listar_ciclos(
    versao: Optional[str] = Query(None, description="Filtrar por versão"),
    projeto_id: Optional[str] = Query(None, description="Filtrar por projeto"),
    current_user_id: str = Depends(get_current_user)
):
    """Lista todos os ciclos ou filtra por versão/projeto."""
    conn_instance = Connection()
    conn = conn_instance.get_conn()
    
    try:
        if projeto_id:
            ciclos = await CicloService.get_ciclos_by_projeto(conn, projeto_id)
        elif versao:
            ciclos = await CicloService.get_ciclos_by_versao(conn, versao)
        else:
            ciclos = await CicloService.get_all_ciclos(conn)
        return ciclos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
    finally:
        conn_instance.release_conn(conn)

@router.get("/projeto/{projeto_id}", response_model=List[CicloResponseDTO])
async def listar_ciclos_por_projeto(
    projeto_id: str,
    current_user_id: str = Depends(get_current_user)
):
    """Lista todos os ciclos de um projeto específico."""
    conn_instance = Connection()
    conn = conn_instance.get_conn()
    
    try:
        ciclos = await CicloService.get_ciclos_by_projeto(conn, projeto_id)
        return ciclos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
    finally:
        conn_instance.release_conn(conn)

@router.get("/nome/{nome}", response_model=CicloResponseDTO)
async def obter_ciclo_por_nome(
    nome: str,
    current_user_id: str = Depends(get_current_user)
):
    """Obtém um ciclo pelo nome."""
    conn_instance = Connection()
    conn = conn_instance.get_conn()
    
    try:
        ciclo = await CicloService.get_ciclo_by_nome(conn, nome)
        if not ciclo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ciclo não encontrado"
            )
        return ciclo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
    finally:
        conn_instance.release_conn(conn)

@router.get("/{ciclo_id}", response_model=CicloResponseDTO)
async def obter_ciclo(
    ciclo_id: str,
    current_user_id: str = Depends(get_current_user)
):
    """Obtém um ciclo pelo ID."""
    conn_instance = Connection()
    conn = conn_instance.get_conn()
    
    try:
        ciclo = await CicloService.get_ciclo_by_id(conn, ciclo_id)
        if not ciclo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ciclo não encontrado"
            )
        return ciclo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
    finally:
        conn_instance.release_conn(conn)

@router.put("/{ciclo_id}", response_model=CicloResponseDTO)
async def atualizar_ciclo(
    ciclo_id: str, 
    ciclo_data: CicloUpdateDTO,
    current_user_id: str = Depends(get_current_user)
):
    """Atualiza um ciclo."""
    conn_instance = Connection()
    conn = conn_instance.get_conn()
    
    try:
        updated_ciclo = await CicloService.update_ciclo(conn, ciclo_id, ciclo_data)
        if not updated_ciclo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ciclo não encontrado"
            )
        return updated_ciclo
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

@router.delete("/{ciclo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_ciclo(
    ciclo_id: str,
    current_user_id: str = Depends(get_current_user)
):
    """Deleta um ciclo."""
    conn_instance = Connection()
    conn = conn_instance.get_conn()
    
    try:
        deleted = await CicloService.delete_ciclo(conn, ciclo_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ciclo não encontrado"
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