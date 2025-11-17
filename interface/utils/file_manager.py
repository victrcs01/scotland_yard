import json
import os
from tkinter import messagebox
from PIL import Image, ImageFilter
from typing import Dict, Any, Tuple

# Constantes
DATA_DIR = "data"
NOME_ARQUIVO_JOGADORES = os.path.join(DATA_DIR, "jogadores.json")
NOME_ARQUIVO_CASOS = os.path.join(DATA_DIR, "data.json")
NOME_IMAGEM_BACKGROUND = os.path.join(DATA_DIR, "background.png")

class fileManager:
    """Gerencia o carregamento e salvamento de arquivos de dados do jogo."""

    def __init__(self) -> None:
        """Inicializa o fileManager, garantindo que o diretório de dados exista."""
        os.makedirs(DATA_DIR, exist_ok=True)
    
    def carregar_dados_casos(self) -> Dict[str, Any]:
        """
        Carrega os dados dos casos do arquivo JSON.

        Returns:
            Dict[str, Any]: Um dicionário com os dados dos casos.
        """
        if not os.path.exists(NOME_ARQUIVO_CASOS):
            messagebox.showerror("Erro Crítico", f"Arquivo de casos '{NOME_ARQUIVO_CASOS}' não encontrado!")
            return {"casos": {}}
        try:
            with open(NOME_ARQUIVO_CASOS, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            messagebox.showerror("Erro Crítico", f"Arquivo '{NOME_ARQUIVO_CASOS}' está corrompido.")
            return {"casos": {}}
        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Erro ao ler '{NOME_ARQUIVO_CASOS}': {e}")
            return {"casos": {}}

    def carregar_dados_jogadores(self) -> Dict[str, Any]:
        """
        Carrega os dados dos jogadores do arquivo JSON.

        Returns:
            Dict[str, Any]: Um dicionário com os dados dos jogadores.
        """
        if not os.path.exists(NOME_ARQUIVO_JOGADORES):
            return {}
        try:
            with open(NOME_ARQUIVO_JOGADORES, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                return dados if isinstance(dados, dict) else {}
        except (json.JSONDecodeError, IOError):
            return {}

    def salvar_dados_jogadores(self, dados: Dict[str, Any]) -> None:
        """
        Salva os dados dos jogadores em um arquivo JSON.

        Args:
            dados (Dict[str, Any]): Os dados dos jogadores a serem salvos.
        """
        try:
            with open(NOME_ARQUIVO_JOGADORES, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
        except IOError as e:
            messagebox.showwarning("Erro ao Salvar", f"Não foi possível salvar seu progresso: {e}")

    def carregar_imagens_bg(self) -> Tuple[Image.Image, Image.Image]:
        """
        Carrega a imagem de fundo e cria uma versão desfocada.

        Returns:
            Tuple[Image.Image, Image.Image]: Uma tupla contendo a imagem original e a imagem desfocada.
        """
        original_image = Image.open(NOME_IMAGEM_BACKGROUND)
        blurred_image = original_image.filter(ImageFilter.GaussianBlur(radius=10))
        return original_image, blurred_image
