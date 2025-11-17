from __future__ import annotations
from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.jogo.pistas.pista import Pista
    from src.jogo.personagens.npc import NPC

class Local:
    """Representa um local no mapa do jogo."""

    def __init__(self, nome: str, descricao: str) -> None:
        """
        Inicializa um objeto Local.

        Args:
            nome (str): O nome do local.
            descricao (str): A descrição do local.
        """
        self.nome: str = nome
        self.descricao: str = descricao
        self.conexoes: Dict[str, Local] = {}
        self.pistas: List[Pista] = []
        self.npcs: List[NPC] = []

    def adicionar_conexao(self, direcao: str, local: Local) -> None:
        """
        Adiciona uma conexão a outro local.

        Args:
            direcao (str): A direção da conexão (ex: "norte", "sul").
            local (Local): O objeto Local para o qual a conexão leva.
        """
        self.conexoes[direcao] = local

    def get_info(self) -> str:
        """
        Retorna uma descrição formatada do local, incluindo pistas, NPCs e saídas.

        Returns:
            str: As informações do local.
        """
        info = f"--- 📍 {self.nome} ---\n{self.descricao}\n\n"
        if self.pistas:
            info += "🔎 Pistas no local: " + ", ".join([p.nome for p in self.pistas]) + "\n"
        if self.npcs:
            info += "👥 Pessoas presentes: " + ", ".join([n.nome for n in self.npcs]) + "\n"
        
        info += "\n🚪 Saídas: " + ", ".join(self.conexoes.keys())
        return info
