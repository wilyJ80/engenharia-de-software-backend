from src.model.artefato import Artefato, ArtefatoBase, ArtefatoResponse
from src.repository import artefato_repository


async def create_artefato(
    #db,
    artefato: ArtefatoBase,
) -> Artefato | None:

    existing_artefato = await artefato_repository.get_artefato_by_name(artefato.nome)
    if existing_artefato:
        return None

    inserted_artefato = await artefato_repository.create_artefato(artefato)

    return inserted_artefato

async def get_all_artefatos() -> ArtefatoResponse | None:
    return await artefato_repository.get_all_artefatos()

async def get_artefato_by_id(artefato_id: str) -> ArtefatoResponse | None:
    return await artefato_repository.get_artefato_by_id(artefato_id)

async def delete_artefato(artefato_id: str) -> ArtefatoResponse | None:
    return await artefato_repository.delete_artefato(artefato_id)

async def update_artefato(artefato_id: str, artefato: ArtefatoBase) -> ArtefatoResponse | None:
    existing_artefato = await artefato_repository.get_artefato_by_name(artefato.nome)
    if existing_artefato:
        return None
    
    return await artefato_repository.update_artefato(artefato_id, artefato)