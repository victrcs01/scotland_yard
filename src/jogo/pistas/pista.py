from typing import Type

class Pista:
    """Representa uma pista genérica no jogo."""

    def __init__(self, nome: str, descricao: str) -> None:
        """
        Inicializa um objeto Pista.

        Args:
            nome (str): O nome ou título da pista.
            descricao (str): A descrição detalhada da pista.
        """
        self.nome: str = nome
        self.descricao: str = descricao

    def examinar(self) -> str:
        """
        Retorna uma descrição formatada da pista.

        Returns:
            str: A descrição da pista.
        """
        return f"Pista: {self.nome}\nDetalhe: {self.descricao}"
