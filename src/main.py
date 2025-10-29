from fastapi import FastAPI
from routes.fase_routes import fase_router
from routes.example_route import router as exampleRouter

app = FastAPI()

app.include_router(exampleRouter)
app.include_router(fase_router)