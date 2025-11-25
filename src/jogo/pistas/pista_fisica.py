from src.jogo.pistas.pista import Pista

class PistaFisica(Pista):
    """Representa uma pista física ou um objeto encontrado na cena do crime."""

    def __init__(self, nome: str, descricao: str, local_encontrado: str) -> None:
        """
        Inicializa um objeto PistaFisica.

        Args:
            nome (str): O nome do objeto ou pista.
            descricao (str): A descrição ou análise do objeto.
            local_encontrado (str): O local onde a pista foi encontrada.
        """
        super().__init__(nome, descricao)
        self.local_encontrado: str = local_encontrado

    def examinar(self) -> str:
        """
        Retorna uma descrição formatada da pista física.

        Returns:
            str: A descrição da pista.
        """
        return f"[OBJETO] {self.nome} (Encontrado em: {self.local_encontrado})\nAnálise: {self.descricao}"
