from src.jogo.personagens.npc import NPC

class Suspeito(NPC):
    def __init__(self, nome, dialogo_inicial, culpado=False, alibi=""):
        super().__init__(nome, dialogo_inicial)
        self.culpado = culpado
        self.alibi = alibi

    def ser_acusado(self):
        if self.culpado:
            return True, f"\n🚨 {self.nome}: 'Tudo bem, fui eu!'"
        else:
            return False, f"\n😠 {self.nome}: 'Você está louco? Eu estava {self.alibi}!'"