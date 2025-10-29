from fastapi import FastAPI

from routes.example_route import router as exampleRouter
from src.routes import artefatos_router

app = FastAPI()

app.include_router(exampleRouter)

app.include_router(artefatos_router)