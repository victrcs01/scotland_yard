
import json
import os
from tkinter import messagebox
from PIL import Image, ImageFilter

# Constantes
DATA_DIR = "data"
NOME_ARQUIVO_JOGADORES = os.path.join(DATA_DIR, "jogadores.json")
NOME_ARQUIVO_CASOS = os.path.join(DATA_DIR, "data.json")
NOME_IMAGEM_BACKGROUND = os.path.join(DATA_DIR, "background.png")

class fileManager:
    
    def __init__(self):
        # Garante que o diretório de dados exista ao salvar
        os.makedirs(DATA_DIR, exist_ok=True)
    
    def carregar_dados_casos(cls):
        if not os.path.exists(NOME_ARQUIVO_CASOS):
            messagebox.showerror("Erro Crítico", f"Arquivo de casos '{NOME_ARQUIVO_CASOS}' não encontrado!")
            return {"casos": {}} # Retorna vazio para evitar crash
        try:
            with open(NOME_ARQUIVO_CASOS, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            messagebox.showerror("Erro Crítico", f"Arquivo '{NOME_ARQUIVO_CASOS}' está corrompido.")
            return {"casos": {}}
        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Erro ao ler '{NOME_ARQUIVO_CASOS}': {e}")
            return {"casos": {}}


    def carregar_dados_jogadores(cls):
        if not os.path.exists(NOME_ARQUIVO_JOGADORES):
            return {} # Ok não existir, será criado
        try:
            with open(NOME_ARQUIVO_JOGADORES, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                return dados if isinstance(dados, dict) else {} # Garante que é um dict
        except (json.JSONDecodeError, IOError):
            return {} # Retorna vazio se corrompido ou ilegível

    def salvar_dados_jogadores(cls, dados):
        try:
            with open(NOME_ARQUIVO_JOGADORES, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
        except IOError as e:
            messagebox.showwarning("Erro ao Salvar", f"Não foi possível salvar seu progresso: {e}")

    def carregar_imagens_bg(cls):

        # Carrega a imagem de fundo e aplica um desfoque
        original_image = Image.open(NOME_IMAGEM_BACKGROUND)
        blurred_image = original_image.filter(ImageFilter.GaussianBlur(radius=10))
        return original_image, blurred_image
    