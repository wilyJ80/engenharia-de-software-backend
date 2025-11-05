from enum import Enum

class CardStatus(str, Enum):
    """
    Status possíveis para um Card.
    """
    A_FAZER = "a_fazer"
    EM_ANDAMENTO = "em_andamento"
    TESTES_VALIDACAO = "testes_validacao"
    CONCLUIDO = "concluido"
