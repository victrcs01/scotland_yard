from src.jogo.pistas.pista import Pista

class PistaVerbal(Pista):
    """Representa uma informação obtida verbalmente de uma testemunha."""

    def __init__(self, nome: str, descricao: str, testemunha: str) -> None:
        """
        Inicializa um objeto PistaVerbal.

        Args:
            nome (str): Um título para o depoimento.
            descricao (str): O conteúdo do depoimento.
            testemunha (str): O nome da testemunha que deu o depoimento.
        """
        super().__init__(nome, descricao)
        self.testemunha: str = testemunha

    def examinar(self) -> str:
        """
        Retorna o depoimento formatado.

        Returns:
            str: O depoimento da testemunha.
        """
        return f"[DEPOIMENTO] De: {self.testemunha}\nRelato: \"{self.descricao}\""
