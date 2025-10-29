# src/model/__init__.py

from ._common import CardStatus

from .projeto_usuario import ProjetoUsuario
from .fase_artefato import FaseArtefato

from .usuario import Usuario
from .projeto import Projeto
from .fase import Fase
from .artefato import Artefato
from .ciclo import Ciclo
from .card import Card

print("Modelos do gps-SuperA carregados.")