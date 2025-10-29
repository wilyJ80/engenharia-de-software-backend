import os
from dotenv import load_dotenv

from pathlib import Path

# |=======| ACESSANDO O ARQUIVO '.env' (VARIÁVEIS DE AMBIENTE) |=======|
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# |=======| CONFIGUTAÇÃO DO PROJETO |=======|
class Settings:
    PROJECT_NAME   : str = "supera"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER     : str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD : str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST     : str = os.getenv("POSTGRES_HOST","localhost")
    POSTGRES_PORT     : str = os.getenv("POSTGRES_PORT", "5434") # PORTA PADRÃO DO POSTGRE É 5434
    POSTGRES_DATABASE : str = os.getenv("POSTGRES_DATABASE","tdd")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

settings = Settings()