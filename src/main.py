from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes.artefatos_router import router as artefatos_router
from routes.fase_routes import fase_router as fase_routes
from routes.ciclo_routes import router as ciclo_router
from routes.projeto_router import router as projeto_router
from routes.card_routes import router as card_router
import uvicorn

from routes.example_route import router as exampleRouter
from routes.usuario_route import router as usuarioRouter

# Configuração da aplicação FastAPI
app = FastAPI(
    title="API Backend - Sistema de Gerenciamento de Projetos",
    description="API para gerenciamento de usuários, ciclos, fases e artefatos com autenticação JWT e operações CRUD completas",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configuração CORS para desenvolvimento
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint raiz
@app.get("/", tags=["Health Check"])
async def root():
    """Endpoint de verificação de saúde da API"""
    return {
        "message": "API Backend está funcionando!",
        "status": "online",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Endpoint de health check
@app.get("/health", tags=["Health Check"])
async def health_check():
    """Endpoint para verificar se a API está funcionando"""
    return {"status": "healthy", "service": "usuario-api"}

# Inclusão das rotas
app.include_router(exampleRouter)
app.include_router(usuarioRouter)
app.include_router(artefatos_router)
app.include_router(fase_routes)
app.include_router(ciclo_router)
app.include_router(projeto_router)
app.include_router(card_router)

# Manipulador de exceções global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Manipulador global de exceções"""
    return JSONResponse(
        status_code=500,
        content={
            "message": "Erro interno do servidor",
            "error": str(exc) if app.debug else "Internal server error"
        }
    )

# Configuração para executar diretamente
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )