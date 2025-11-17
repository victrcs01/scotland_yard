from src.jogo.personagens.npc import NPC

class Testemunha(NPC):
    def __init__(self, nome, dialogo_inicial, pista_chave=None):
        super().__init__(nome, dialogo_inicial)
        self.pista_chave = pista_chave
        self.pista_entregue = False

    def conversar(self, detetive):
        dialogo_base = super().conversar(detetive)
        
        if self.pista_chave and not self.pista_entregue:
            detetive.adicionar_pista(self.pista_chave)
            self.pista_entregue = True
            dialogo_base += f"\n👀 {self.nome} te entrega uma anotação discretamente."
        
        return dialogo_base