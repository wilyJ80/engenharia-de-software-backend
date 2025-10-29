from datetime import datetime
from typing import Optional, List
from model.usuario import Usuario
from model.dto.usuario_dto import UsuarioCreateDTO, UsuarioResponseDTO
from core.auth import get_password_hash, verify_password
import uuid

# Simulação de banco de dados em memória (substitua por implementação real)
fake_users_db = {}

class UsuarioService:
    
    @staticmethod
    def create_user(usuario_data: UsuarioCreateDTO) -> UsuarioResponseDTO:
        """Cria um novo usuário."""
        # Verifica se o email já existe
        for user in fake_users_db.values():
            if user.email == usuario_data.email:
                raise ValueError("Email já cadastrado")
        
        # Gera ID único
        user_id = str(uuid.uuid4())
        
        # Hash da senha
        senha_hash = get_password_hash(usuario_data.senha)
        
        # Cria o usuário
        usuario = Usuario(
            id=user_id,
            nome=usuario_data.nome,
            email=usuario_data.email,
            senha_hash=senha_hash,
            created_at=datetime.utcnow(),
            updated_at=None
        )
        
        # Salva no "banco de dados"
        fake_users_db[user_id] = usuario
        
        # Retorna resposta sem a senha
        return UsuarioResponseDTO(
            id=usuario.id,
            nome=usuario.nome,
            email=usuario.email
        )
    
    @staticmethod
    def authenticate_user(email: str, senha: str) -> Optional[Usuario]:
        """Autentica um usuário."""
        for user in fake_users_db.values():
            if user.email == email:
                if verify_password(senha, user.senha_hash):
                    return user
        return None
    
    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[UsuarioResponseDTO]:
        """Obtém um usuário pelo ID."""
        user = fake_users_db.get(user_id)
        if user:
            return UsuarioResponseDTO(
                id=user.id,
                nome=user.nome,
                email=user.email
            )
        return None
    
    @staticmethod
    def get_all_users() -> List[UsuarioResponseDTO]:
        """Obtém todos os usuários."""
        return [
            UsuarioResponseDTO(
                id=user.id,
                nome=user.nome,
                email=user.email
            )
            for user in fake_users_db.values()
        ]
    
    @staticmethod
    def update_user(user_id: str, usuario_data: UsuarioCreateDTO) -> Optional[UsuarioResponseDTO]:
        """Atualiza um usuário."""
        user = fake_users_db.get(user_id)
        if not user:
            return None
        
        # Verifica se o novo email já existe (exceto para o próprio usuário)
        for uid, u in fake_users_db.items():
            if uid != user_id and u.email == usuario_data.email:
                raise ValueError("Email já cadastrado")
        
        # Atualiza os dados
        user.nome = usuario_data.nome
        user.email = usuario_data.email
        user.senha_hash = get_password_hash(usuario_data.senha)
        user.updated_at = datetime.utcnow()
        
        fake_users_db[user_id] = user
        
        return UsuarioResponseDTO(
            id=user.id,
            nome=user.nome,
            email=user.email
        )
    
    @staticmethod
    def delete_user(user_id: str) -> bool:
        """Deleta um usuário."""
        if user_id in fake_users_db:
            del fake_users_db[user_id]
            return True
        return False