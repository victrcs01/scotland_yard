from src.jogo.pistas.pista import Pista

class PistaDocumental(Pista):
    """Representa uma pista encontrada em um documento."""

    def __init__(self, nome: str, descricao: str, local_encontrado: str) -> None:
        """
        Inicializa um objeto PistaDocumental.

        Args:
            nome (str): O nome do documento.
            descricao (str): O conteúdo ou descrição do documento.
            local_encontrado (str): O local onde o documento foi encontrado.
        """
        super().__init__(nome, descricao)
        self.local_encontrado: str = local_encontrado

    def examinar(self) -> str:
        """
        Retorna uma descrição formatada da pista documental.

        Returns:
            str: A descrição da pista.
        """
        return f"[DOCUMENTO] {self.nome} (Local: {self.local_encontrado})\nConteúdo: {self.descricao}"
