from src.jogo.pistas.pista import Pista

class PistaVerbal(Pista):
    def __init__(self, nome, descricao, testemunha):
        super().__init__(nome, descricao)
        self.testemunha = testemunha

    def examinar(self):
        return f"[DEPOIMENTO] De: {self.testemunha}\nRelato: \"{self.descricao}\""