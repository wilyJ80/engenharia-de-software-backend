from src.model.artefato import Artefato, ArtefatoBase
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