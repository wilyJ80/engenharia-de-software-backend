# Estrutura do Service - PostgreSQL Ready

## 📋 Visão Geral

A estrutura do `UsuarioService` foi completamente reformulada para suportar PostgreSQL de forma assíncrona, seguindo padrões de arquitetura limpa e injeção de dependências.

## 🏗️ Arquitetura

### 1. **Repository Pattern**
```
IUsuarioRepository (Interface)
├── InMemoryUsuarioRepository (Desenvolvimento/Testes)
└── PostgreSQLUsuarioRepository (Produção)
```

### 2. **Service Layer**
- `UsuarioService`: Lógica de negócio
- Recebe `IUsuarioRepository` via injeção de dependências
- Métodos assíncronos prontos para PostgreSQL

### 3. **Factory Pattern**
- `ServiceFactory`: Cria serviços com dependências corretas
- Funções auxiliares para FastAPI dependencies

## 🚀 Como Usar

### Desenvolvimento (In-Memory)
```python
from service.service_factory import ServiceFactory

# Criar service com repositório em memória
service = ServiceFactory.create_usuario_service_in_memory()

# Usar o service
user_dto = UsuarioCreateDTO(nome="João", email="joao@email.com", senha="123456")
new_user = await service.create_user(user_dto)
```

### Produção (PostgreSQL)
```python
from service.service_factory import ServiceFactory
from db.database import get_db_session

# Com sessão do banco
async for session in get_db_session():
    service = ServiceFactory.create_usuario_service_postgresql(session)
    user_dto = UsuarioCreateDTO(nome="João", email="joao@email.com", senha="123456")
    new_user = await service.create_user(user_dto)
```

### FastAPI Integration
```python
from fastapi import Depends
from service.service_factory import get_usuario_service_postgresql

@app.post("/usuarios/")
async def criar_usuario(
    usuario_data: UsuarioCreateDTO,
    service: UsuarioService = Depends(get_usuario_service_postgresql)
):
    return await service.create_user(usuario_data)
```

## 📦 Dependências Necessárias

```bash
pip install sqlalchemy[asyncio] asyncpg alembic
```

## ⚙️ Configuração do Banco

### 1. Variáveis de Ambiente
```bash
# .env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
USE_POSTGRESQL=true
```

### 2. Criar Tabelas
```python
from db.database import create_tables

# Executar uma vez para criar as tabelas
await create_tables()
```

## 🔄 Migração do Código Antigo

### Antes:
```python
# Service estático com banco em memória
user = UsuarioService.create_user(user_data)
```

### Depois:
```python
# Service com injeção de dependências
service = ServiceFactory.create_usuario_service_in_memory()
user = await service.create_user(user_data)
```

## 🧪 Testes

### Exemplo de Teste Unitário
```python
import pytest
from service.service_factory import ServiceFactory

@pytest.mark.asyncio
async def test_create_user():
    # Arrange
    service = ServiceFactory.create_usuario_service_in_memory()
    user_data = UsuarioCreateDTO(nome="Test", email="test@email.com", senha="123")
    
    # Act
    result = await service.create_user(user_data)
    
    # Assert
    assert result.nome == "Test"
    assert result.email == "test@email.com"
```

## 📂 Estrutura de Arquivos Criada

```
src/
├── db/
│   └── database.py           # Configuração SQLAlchemy + PostgreSQL
├── model/
│   ├── usuario.py            # Modelo Pydantic (domínio)
│   ├── usuario_table.py      # Modelo SQLAlchemy (banco)
│   └── dto/
│       └── usuario_dto.py    # DTOs para API
├── repository/
│   └── usuario_repository.py # Interface + Implementações
└── service/
    ├── usuario_service.py    # Service refatorado
    └── service_factory.py    # Factory para DI
```

## ✅ Vantagens da Nova Estrutura

1. **Testabilidade**: Fácil mock do repository nos testes
2. **Flexibilidade**: Troca entre in-memory e PostgreSQL sem alterar código
3. **Escalabilidade**: Pronto para outros bancos de dados
4. **Manutenibilidade**: Separação clara de responsabilidades
5. **Async/Await**: Performance otimizada para I/O
6. **Type Safety**: Tipagem completa com interfaces

## 🔧 Próximos Passos

1. Implementar `PostgreSQLUsuarioRepository` com SQLAlchemy
2. Configurar Alembic para migrações
3. Adicionar logs e métricas
4. Implementar cache (Redis)
5. Adicionar transações distribuídas