from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from typing import List

from model.dto.usuario_dto import UsuarioCreateDTO, UsuarioResponseDTO, UsuarioLoginDTO
from model.token import Token
from service.usuario_service import UsuarioService
from core.auth import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from db.connection import Connection

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/registro", response_model=UsuarioResponseDTO, status_code=status.HTTP_201_CREATED)
async def criar_usuario(usuario: UsuarioCreateDTO):
    """Registra um novo usuário."""
    conn_instance = Connection()
    conn = conn_instance.get_conn()
    
    try:
        result = await UsuarioService.create_user(conn, usuario)
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

@router.post("/login", response_model=Token)
async def login_usuario(usuario_login: UsuarioLoginDTO):
    """Autentica um usuário e retorna um token JWT."""
    conn_instance = Connection()
    conn = conn_instance.get_conn()
    
    try:
        user = await UsuarioService.authenticate_user(conn, usuario_login.email, usuario_login.senha)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
    finally:
        conn_instance.release_conn(conn)

@router.get("/me", response_model=UsuarioResponseDTO)
async def obter_usuario_atual(current_user_id: str = Depends(get_current_user)):
    """Obtém as informações do usuário atualmente autenticado."""
    conn_instance = Connection()
    conn = conn_instance.get_conn()
    
    try:
        user = await UsuarioService.get_user_by_id(conn, current_user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
    finally:
        conn_instance.release_conn(conn)

@router.get("/", response_model=List[UsuarioResponseDTO])
async def listar_usuarios(current_user_id: str = Depends(get_current_user)):
    """Lista todos os usuários (requer autenticação)."""
    conn_instance = Connection()
    conn = conn_instance.get_conn()
    
    try:
        users = await UsuarioService.get_all_users(conn)
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
    finally:
        conn_instance.release_conn(conn)


@router.get("/{user_id}", response_model=UsuarioResponseDTO)
async def obter_usuario(user_id: str, current_user_id: str = Depends(get_current_user)):
    """Obtém um usuário pelo ID (requer autenticação)."""
    conn_instance = Connection()
    conn = conn_instance.get_conn()
    
    try:
        user = await UsuarioService.get_user_by_id(conn, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
    finally:
        conn_instance.release_conn(conn)

@router.put("/{user_id}", response_model=UsuarioResponseDTO)
async def atualizar_usuario(
    user_id: str, 
    usuario_data: UsuarioCreateDTO,
    current_user_id: str = Depends(get_current_user)
):
    """Atualiza um usuário (requer autenticação). Qualquer usuário autenticado pode atualizar qualquer usuário."""
    conn_instance = Connection()
    conn = conn_instance.get_conn()
    
    try:
        updated_user = await UsuarioService.update_user(conn, user_id, usuario_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return updated_user
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

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_usuario(
    user_id: str,
    current_user_id: str = Depends(get_current_user)
):
    """Deleta um usuário (requer autenticação). Qualquer usuário autenticado pode deletar qualquer usuário."""
    conn_instance = Connection()
    conn = conn_instance.get_conn()
    
    try:
        deleted = await UsuarioService.delete_user(conn, user_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
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
