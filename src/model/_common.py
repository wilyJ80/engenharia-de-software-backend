# src/model/_common.py
import enum

class CardStatus(str, enum.Enum):
    """Define os estados possíveis do card no Kanban."""
    a_fazer = "a_fazer"
    em_andamento = "em_andamento"
    validacao = "validacao"
    concluido = "concluido"