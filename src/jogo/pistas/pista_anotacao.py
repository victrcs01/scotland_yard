from src.jogo.pistas.pista import Pista

class PistaAnotacao(Pista):
    """Representa uma anotação feita pelo jogador."""

    def __init__(self, descricao: str) -> None:
        """
        Inicializa um objeto PistaAnotacao.

        Args:
            descricao (str): O conteúdo da anotação.
        """
        super().__init__("Anotação Pessoal", descricao)

    def examinar(self) -> str:
        """
        Retorna a anotação formatada.

        Returns:
            str: A anotação do jogador.
        """
        return f"📝 [ANOTAÇÃO PESSOAL]\n{self.descricao}"
