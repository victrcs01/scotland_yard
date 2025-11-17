from src.jogo.pistas.pista import Pista

class PistaAnotacao(Pista):
    def __init__(self, descricao):
        super().__init__("Anotação Pessoal", descricao)

    def examinar(self):
        return f"📝 [ANOTAÇÃO PESSOAL]\n{self.descricao}"