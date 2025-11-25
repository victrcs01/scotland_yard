from __future__ import annotations
from typing import Optional
from typing import TYPE_CHECKING

from src.jogo.personagens.npc import NPC
from src.jogo.pistas.pista import Pista

if TYPE_CHECKING:
    from src.jogo.detetive import Detetive

class Testemunha(NPC):
    """Representa uma testemunha que pode fornecer uma pista ao detetive."""

    def __init__(self, nome: str, dialogo_inicial: str, pista_chave: Optional[Pista] = None) -> None:
        """
        Inicializa um objeto Testemunha.

        Args:
            nome (str): O nome da testemunha.
            dialogo_inicial (str): O diálogo inicial da testemunha.
            pista_chave (Optional[Pista], optional): A pista que a testemunha pode fornecer. Defaults to None.
        """
        super().__init__(nome, dialogo_inicial)
        self.pista_chave: Optional[Pista] = pista_chave
        self.pista_entregue: bool = False

    def conversar(self, detetive: Detetive) -> str:
        """
        Inicia uma conversa com a testemunha, potencialmente entregando uma pista.

        Args:
            detetive (Detetive): O objeto detetive que está interagindo.

        Returns:
            str: O diálogo da testemunha.
        """
        dialogo_base = super().conversar(detetive)
        
        if self.pista_chave and not self.pista_entregue:
            detetive.adicionar_pista(self.pista_chave)
            self.pista_entregue = True
            dialogo_base += f"\n👀 {self.nome} te entrega uma anotação discretamente."
        
        return dialogo_base
