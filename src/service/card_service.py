from datetime import datetime
from typing import Optional, List
from psycopg2.extensions import connection # Assumindo que você usa psycopg2 para conexão
from model.card import CardModel # Seu modelo de dados
from model.dto.card_dto import CardCreateDTO, CardUpdateDTO, CardResponseDTO
from repository import card_repository # O repositório a ser implementado
from utils.functions import print_error_details
from model.card_status import CardStatus

import traceback

class CardService:

    @staticmethod
    async def create_card(conn: connection, card_data: CardCreateDTO) -> CardResponseDTO:
        """Cria um novo card."""
        try:
            # Não há validação de unicidade de "nome" como em Ciclo, mas você pode adicionar
            # validações de existência dos IDs associados (ciclo, fase, artefato, responsável) aqui.

            # Cria o card no banco
            created_card = await card_repository.create_card(conn, card_data)

            if not created_card:
                raise ValueError("Erro ao criar card")

            # Retorna resposta
            return CardResponseDTO(
                id=created_card['id'],
                status=created_card['status'],
                tempo_planejado_horas=created_card['tempo_planejado_horas'],
                link=created_card['link'],
                descricao=created_card['descricao'],
                ciclo_id=created_card['ciclo_id'],
                fase_id=created_card['fase_id'],
                artefato_id=created_card['artefato_id'],
                responsavel_id=created_card['responsavel_id']
            )
        except Exception as e:
            print_error_details(e)
            raise e


    @staticmethod
    async def get_card_by_id(conn: connection, card_id: str) -> Optional[CardResponseDTO]:
        """Obtém um card pelo ID."""
        try:
            card_data = await card_repository.get_card_by_id(conn, card_id)
            if card_data:
                return CardService._map_to_response_dto(card_data) # Usa função auxiliar
            return None
        except Exception as e:
            print_error_details(e)
            return None

    @staticmethod
    async def get_all_cards(conn: connection) -> List[CardResponseDTO]:
        """Obtém todos os cards sem filtro."""
        try:
            cards_data = await card_repository.get_all_cards(conn)
            print("CARDS DATA: ", cards_data)
            return [CardService._map_to_response_dto(card) for card in cards_data]
        except Exception as e:
            print_error_details(e)
            print(traceback.format_exc())
            return []

    @staticmethod
    async def update_card(conn: connection, card_id: str, card_data: CardUpdateDTO) -> Optional[CardResponseDTO]:
        """Atualiza um card. Aceita apenas os campos fornecidos no DTO."""
        try:
            # 1. Verifica se o card existe
            existing_card = await card_repository.get_card_by_id(conn, card_id)
            if not existing_card:
                return None # Retorna None se não encontrar

            # 2. Converte o DTO para um dicionário, ignorando campos None
            update_data = card_data.model_dump(exclude_none=True)

            # 3. Se não houver dados para atualizar, retorna o card existente
            if not update_data:
                return CardService._map_to_response_dto(existing_card)

            # 4. Atualiza o card
            updated_card = await card_repository.update_card(conn, card_id, update_data)

            if updated_card:
                return CardService._map_to_response_dto(updated_card)
            return None
        except Exception as e:
            print_error_details(e)
            raise e

    @staticmethod
    async def delete_card(conn: connection, card_id: str) -> bool:
        """Deleta um card."""
        try:
            deleted_count = await card_repository.delete_card(conn, card_id)
            return deleted_count > 0 # Retorna True se pelo menos 1 registro foi deletado
        except Exception as e:
            print_error_details(e)
            return False

    @staticmethod
    async def get_cards_by_status(conn: connection, status_val: CardStatus) -> List[CardResponseDTO]:
        """Obtém cards por status."""
        try:
            cards_data = await card_repository.get_cards_by_status(conn, status_val.value)
            return [CardService._map_to_response_dto(card) for card in cards_data]
        except Exception as e:
            print_error_details(e)
            return []

    @staticmethod
    async def get_cards_by_ciclo(conn: connection, ciclo_id: str) -> List[CardResponseDTO]:
        """Obtém cards por ID do ciclo."""
        try:
            cards_data = await card_repository.get_cards_by_ciclo(conn, ciclo_id)
            return [CardService._map_to_response_dto(card) for card in cards_data]
        except Exception as e:
            print_error_details(e)
            return []

    @staticmethod
    async def get_cards_by_responsavel(conn: connection, responsavel_id: str) -> List[CardResponseDTO]:
        """Obtém cards por ID do responsável."""
        try:
            cards_data = await card_repository.get_cards_by_responsavel(conn, responsavel_id)
            return [CardService._map_to_response_dto(card) for card in cards_data]
        except Exception as e:
            print_error_details(e)
            return []

    @staticmethod
    def _map_to_response_dto(card_data: dict) -> CardResponseDTO:
        """Função auxiliar para mapear dados do banco para o DTO de resposta."""
        return CardResponseDTO(
            id=card_data['id'],
            status=CardStatus(card_data['status']), # Converte a string do DB de volta para o Enum
            tempo_planejado_horas=card_data['tempo_planejado_horas'],
            link=card_data['link'],
            descricao=card_data['descricao'],
            ciclo_id=card_data['ciclo_id'],
            fase_id=card_data['fase_id'],
            artefato_id=card_data['artefato_id'],
            responsavel_id=card_data['responsavel_id']
        )