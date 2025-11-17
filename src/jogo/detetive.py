from src.jogo.personagens.suspeito import Suspeito
from src.jogo.pistas.pista_anotacao import PistaAnotacao

class Detetive:
    def __init__(self, nome):
        self.nome = nome
        self.local_atual = None
        self.inventario = []

    def mover(self, direcao):
        if direcao in self.local_atual.conexoes:
            self.local_atual = self.local_atual.conexoes[direcao]
            return True, f"Você viajou para: {self.local_atual.nome}"
        else:
            return False, "🚫 Não há passagem para essa direção."

    def investigar(self):
        if not self.local_atual.pistas:
            return "Não há nada óbvio para investigar aqui."

        pista = self.local_atual.pistas.pop(0) 
        self.adicionar_pista(pista)
        return f"Você coletou: {pista.nome}\n📝 Nova pista adicionada ao caderno."

    def adicionar_pista(self, pista):
        self.inventario.append(pista)

    def fazer_anotacao(self, texto_anotacao):
        if not texto_anotacao:
            return "Você não escreveu nada para anotar."
        nova_anotacao = PistaAnotacao(texto_anotacao)
        self.inventario.append(nova_anotacao)
        return "Sua anotação foi adicionada ao caderno."
        
    def falar_com_npc(self, nome_npc):
        if not nome_npc:
            return "Com quem você quer falar? (Digite o nome no campo)"
            
        npc_alvo = next((n for n in self.local_atual.npcs if n.nome.lower() == nome_npc.lower()), None)
        
        if npc_alvo:
            return npc_alvo.conversar(self)
        else:
            return "Essa pessoa não está aqui."

    def acusar_npc(self, nome_npc):
        if not nome_npc:
            return None, "Quem você quer acusar? (Digite o nome no campo)"

        npc_alvo = next((n for n in self.local_atual.npcs if n.nome.lower() == nome_npc.lower()), None)
        
        if npc_alvo and isinstance(npc_alvo, Suspeito):
            vitoria, mensagem = npc_alvo.ser_acusado()
            return vitoria, mensagem
        elif npc_alvo:
            return None, f"{npc_alvo.nome} é apenas uma testemunha, não faz sentido acusá-lo."
        else:
            return None, "Essa pessoa não está aqui para ser acusada."

    def get_inventario_formatado(self):
        if not self.inventario:
            return "Seu caderno de anotações está vazio."
            
        texto_inventario = "📒 --- SEU CADERNO DE ANOTAÇÕES ---\n\n"
        for i, pista in enumerate(self.inventario):
            texto_inventario += f"{i+1}. {pista.examinar()}\n" + ("-"*20) + "\n"
        return texto_inventario