class NPC:
    def __init__(self, nome, dialogo_inicial):
        self.nome = nome
        self.dialogo_inicial = dialogo_inicial

    def conversar(self, detetive):
        return f"{self.nome} diz: \"{self.dialogo_inicial}\""