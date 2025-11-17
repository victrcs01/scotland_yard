from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.jogo.detetive import Detetive

class NPC:
    """Representa um personagem não-jogável (NPC) genérico no jogo."""

    def __init__(self, nome: str, dialogo_inicial: str) -> None:
        """
        Inicializa um objeto NPC.

        Args:
            nome (str): O nome do NPC.
            dialogo_inicial (str): A fala inicial do NPC.
        """
        self.nome: str = nome
        self.dialogo_inicial: str = dialogo_inicial

    def conversar(self, detetive: Detetive) -> str:
        """
        Retorna o diálogo inicial do NPC.

        Args:
            detetive (Detetive): O objeto detetive que está interagindo com o NPC.

        Returns:
            str: O diálogo do NPC.
        """
        return f'{self.nome} diz: "{self.dialogo_inicial}"'
