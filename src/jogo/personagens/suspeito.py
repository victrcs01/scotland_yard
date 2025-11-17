from src.jogo.personagens.npc import NPC
from typing import Tuple

class Suspeito(NPC):
    """Representa um suspeito no jogo, que pode ou não ser o culpado."""

    def __init__(self, nome: str, dialogo_inicial: str, culpado: bool = False, alibi: str = "") -> None:
        """
        Inicializa um objeto Suspeito.

        Args:
            nome (str): O nome do suspeito.
            dialogo_inicial (str): A fala inicial do suspeito.
            culpado (bool, optional): Se o suspeito é o culpado. Defaults to False.
            alibi (str, optional): O álibi do suspeito. Defaults to "".
        """
        super().__init__(nome, dialogo_inicial)
        self.culpado: bool = culpado
        self.alibi: str = alibi

    def ser_acusado(self) -> Tuple[bool, str]:
        """
        Processa a acusação feita ao suspeito.

        Returns:
            Tuple[bool, str]: Uma tupla contendo um booleano (True se for culpado) e a resposta do suspeito.
        """
        if self.culpado:
            return True, f"\n🚨 {self.nome}: 'Tudo bem, fui eu!'"
        else:
            return False, f"\n😠 {self.nome}: 'Você está louco? Eu estava {self.alibi}!'"
