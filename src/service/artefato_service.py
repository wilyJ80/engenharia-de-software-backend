from src.model.artefato import Artefato, ArtefatoBase, ArtefatoResponse
from src.repository import artefato_repository
from psycopg2.extensions import connection

async def create_artefato(
    db: connection,
    artefato: ArtefatoBase,
) -> Artefato | None:

    existing_artefato = await artefato_repository.get_artefato_by_name(db, artefato.nome)
    if existing_artefato:
        return None

    inserted_artefato = await artefato_repository.create_artefato(artefato)

    return inserted_artefato

async def get_all_artefatos(db: connection,) -> ArtefatoResponse | None:
    return await artefato_repository.get_all_artefatos(db)

async def get_artefato_by_id(db: connection, artefato_id: str) -> ArtefatoResponse | None:
    return await artefato_repository.get_artefato_by_id(db, artefato_id)

async def delete_artefato(db: connection, artefato_id: str) -> ArtefatoResponse | None:
    return await artefato_repository.delete_artefato(db, artefato_id)

async def update_artefato(db: connection, artefato_id: str, artefato: ArtefatoBase) -> ArtefatoResponse | None:
    existing_artefato = await artefato_repository.get_artefato_by_name(db, artefato.nome)
    if existing_artefato:
        return None
    
    return await artefato_repository.update_artefato(db, artefato_id, artefato)