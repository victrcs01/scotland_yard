from __future__ import annotations
from typing import List, Optional, Tuple, TYPE_CHECKING
from src.jogo.personagens.suspeito import Suspeito
from src.jogo.pistas.pista_anotacao import PistaAnotacao

if TYPE_CHECKING:
    from src.jogo.local import Local
    from src.jogo.pistas.pista import Pista

class Detetive:
    """Representa o jogador e suas ações no jogo."""

    def __init__(self, nome: str) -> None:
        """
        Inicializa um objeto Detetive.

        Args:
            nome (str): O nome do detetive.
        """
        self.nome: str = nome
        self.local_atual: Optional[Local] = None
        self.inventario: List[Pista] = []

    def mover(self, direcao: str) -> Tuple[bool, str]:
        """
        Move o detetive para um novo local.

        Args:
            direcao (str): A direção para a qual se mover.

        Returns:
            Tuple[bool, str]: Uma tupla contendo um booleano (True se o movimento foi bem-sucedido) e uma mensagem.
        """
        if self.local_atual and direcao in self.local_atual.conexoes:
            self.local_atual = self.local_atual.conexoes[direcao]
            return True, f"Você viajou para: {self.local_atual.nome}"
        else:
            return False, "🚫 Não há passagem para essa direção."

    def investigar(self) -> str:
        """
        Investiga o local atual em busca de pistas.

        Returns:
            str: Uma mensagem indicando o resultado da investigação.
        """
        if not self.local_atual or not self.local_atual.pistas:
            return "Não há nada óbvio para investigar aqui."

        pista = self.local_atual.pistas.pop(0)
        self.adicionar_pista(pista)
        return f"Você coletou: {pista.nome}\n📝 Nova pista adicionada ao caderno."

    def adicionar_pista(self, pista: Pista) -> None:
        """
        Adiciona uma pista ao inventário do detetive.

        Args:
            pista (Pista): A pista a ser adicionada.
        """
        self.inventario.append(pista)

    def fazer_anotacao(self, texto_anotacao: str) -> str:
        """
        Cria uma anotação pessoal e a adiciona ao inventário.

        Args:
            texto_anotacao (str): O texto da anotação.

        Returns:
            str: Uma mensagem de confirmação.
        """
        if not texto_anotacao:
            return "Você não escreveu nada para anotar."
        nova_anotacao = PistaAnotacao(texto_anotacao)
        self.inventario.append(nova_anotacao)
        return "Sua anotação foi adicionada ao caderno."

    def falar_com_npc(self, nome_npc: str) -> str:
        """
        Inicia uma conversa com um NPC no local atual.

        Args:
            nome_npc (str): O nome do NPC com quem falar.

        Returns:
            str: O diálogo do NPC ou uma mensagem de erro.
        """
        if not nome_npc:
            return "Com quem você quer falar? (Digite o nome no campo)"
            
        if not self.local_atual:
            return "Ocorreu um erro, o detetive não está em lugar nenhum."

        npc_alvo = next((n for n in self.local_atual.npcs if n.nome.lower() == nome_npc.lower()), None)
        
        if npc_alvo:
            return npc_alvo.conversar(self)
        else:
            return "Essa pessoa não está aqui."

    def acusar_npc(self, nome_npc: str) -> Tuple[Optional[bool], str]:
        """
        Acusa um NPC de ser o culpado.

        Args:
            nome_npc (str): O nome do NPC a ser acusado.

        Returns:
            Tuple[Optional[bool], str]: Uma tupla contendo um booleano (True para vitória, False para derrota, None se a acusação for inválida) e uma mensagem.
        """
        if not nome_npc:
            return None, "Quem você quer acusar? (Digite o nome no campo)"

        if not self.local_atual:
            return None, "Ocorreu um erro, o detetive não está em lugar nenhum."

        npc_alvo = next((n for n in self.local_atual.npcs if n.nome.lower() == nome_npc.lower()), None)
        
        if isinstance(npc_alvo, Suspeito):
            vitoria, mensagem = npc_alvo.ser_acusado()
            return vitoria, mensagem
        elif npc_alvo:
            return None, f"{npc_alvo.nome} é apenas uma testemunha, não faz sentido acusá-lo."
        else:
            return None, "Essa pessoa não está aqui para ser acusada."

    def get_inventario_formatado(self) -> str:
        """
        Retorna uma string formatada com todas as pistas do inventário.

        Returns:
            str: O conteúdo do caderno de anotações.
        """
        if not self.inventario:
            return "Seu caderno de anotações está vazio."
            
        texto_inventario = "📒 --- SEU CADERNO DE ANOTAÇÕES ---\n\n"
        for i, pista in enumerate(self.inventario):
            texto_inventario += f"{i+1}. {pista.examinar()}\n" + ("-"*20) + "\n"
        return texto_inventario
