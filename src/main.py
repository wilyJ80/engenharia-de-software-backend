from fastapi import FastAPI

from routes.example_route import router as exampleRouter

app = FastAPI()

app.include_router(exampleRouter)