class Pista:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

    def examinar(self):
        return f"Pista: {self.nome}\nDetalhe: {self.descricao}"