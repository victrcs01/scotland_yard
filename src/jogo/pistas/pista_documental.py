from src.jogo.pistas.pista import Pista

class PistaDocumental(Pista):
    def __init__(self, nome, descricao, local_encontrado):
        super().__init__(nome, descricao)
        self.local_encontrado = local_encontrado

    def examinar(self):
        return f"[DOCUMENTO] {self.nome} (Local: {self.local_encontrado})\nConteúdo: {self.descricao}"