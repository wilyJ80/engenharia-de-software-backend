from fastapi import FastAPI

from routes.example_route import router as exampleRouter
from routes.usuario_route import router as usuarioRouter

app = FastAPI(
    title="API Backend",
    description="API para gerenciamento de usuários com autenticação JWT",
    version="1.0.0"
)

app.include_router(exampleRouter)
app.include_router(usuarioRouter)