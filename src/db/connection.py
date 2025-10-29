import logging
from psycopg2 import pool
from src.core.config import settings
class Connection:
    _instance = None
    _pool = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Connection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            try:
                self._pool = pool.SimpleConnectionPool(
                    minconn=1,
                    maxconn=10,
                    host=settings.POSTGRES_HOST,
                    database=settings.POSTGRES_DATABASE,
                    user=settings.POSTGRES_USER,
                    password=settings.POSTGRES_PASSWORD,
                    port=settings.POSTGRES_PORT
                )
                if not self._pool:
                    raise Exception("Falha ao criar o pool de conexões com o banco")
                self._initialized = True
                print("Conexao criada")
            except Exception as e:
                print(f"Erro ao inicializar pool de conexões: {e}")
                raise

    def get_conn(self):
   
        return self._pool.getconn()

    def release_conn(self, conn):
        self._pool.putconn(conn)

    def close_all(self):
        self._pool.closeall()
        logging.info("🔒 Todas as conexões foram fechadas.")