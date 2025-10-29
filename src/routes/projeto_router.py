from fastapi import APIRouter, status, Depends, HTTPException
from psycopg2.extensions import connection

from db.database import get_db
from model.projeto import Projeto, ProjetoResponse, ProjetoBase
from service.projeto_service import ProjetoService

router = APIRouter(prefix="/projetos", tags=['projetos'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Projeto)
async def create_projeto(projeto: ProjetoBase, db: connection = Depends(get_db)):
    try:
        created = await ProjetoService.create_projeto(db, projeto.dict())
        if not created:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar projeto")
        return created
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")


@router.get("/", response_model=list[Projeto])
async def get_all_projetos(db: connection = Depends(get_db)):
    try:
        projetos = await ProjetoService.get_all_projetos(db)
        return projetos
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")


@router.get("/{projeto_id}", response_model=Projeto)
async def get_projeto_by_id(projeto_id: str, db: connection = Depends(get_db)):
    try:
        projeto = await ProjetoService.get_projeto_by_id(db, projeto_id)
        if not projeto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Projeto não encontrado")
        return projeto
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")


@router.put("/{projeto_id}", response_model=Projeto)
async def update_projeto(projeto_id: str, projeto: ProjetoBase, db: connection = Depends(get_db)):
    try:
        updated = await ProjetoService.update_projeto(db, projeto_id, projeto.dict())
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Projeto não encontrado")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")


@router.delete("/{projeto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_projeto(projeto_id: str, db: connection = Depends(get_db)):
    try:
        deleted = await ProjetoService.delete_projeto(db, projeto_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Projeto não encontrado")
        return
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")
