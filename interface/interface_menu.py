import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from typing import Dict, Any, Optional, List
from interface.utils.file_manager import fileManager
from interface.interface_jogo import JogoFrame

class InterfaceMenu(ctk.CTk):
    """Janela principal do menu do jogo, responsável pelo login e seleção de casos."""

    def __init__(self) -> None:
        """Inicializa a InterfaceMenu."""
        super().__init__()
        self.title("VERITAS - Divisão de Assuntos Acadêmicos")
        self.geometry("1280x720")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.fm: fileManager = fileManager()
        dados_brutos_casos = self.fm.carregar_dados_casos()

        if not dados_brutos_casos.get("casos"):
            messagebox.showerror("Erro Fatal", "Nenhum caso foi encontrado. Verifique o 'data.json'.")
            self.destroy()
            return

        self.dados_casos: Dict[str, Any] = dados_brutos_casos.get("casos", {})
        self.dados_jogadores: Dict[str, Any] = self.fm.carregar_dados_jogadores()
        self.nome_jogador_atual: Optional[str] = None

        self.frame_jogo_atual: Optional[JogoFrame] = None

        try:
            original_image, blurred_image = self.fm.carregar_imagens_bg()
            self.bg_image_login = ctk.CTkImage(original_image, size=(1280, 720))
            self.bg_image_casos = ctk.CTkImage(blurred_image, size=(1280, 720))
        except FileNotFoundError:
            self.bg_image_login = self.bg_image_casos = None

        self.bg_label = ctk.CTkLabel(self, text="", image=self.bg_image_login)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.lower()

        self.frame_login = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_casos = ctk.CTkFrame(self, fg_color="transparent")

        self.criar_widgets_login()
        self.criar_widgets_casos()

        self.frame_login.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def criar_widgets_login(self) -> None:
        """Cria os widgets da tela de login."""
        ctk.CTkLabel(self.frame_login, text="VERITAS", font=("Segoe UI", 32, "bold")).pack(pady=(20, 10))
        ctk.CTkLabel(self.frame_login, text="Divisão de Assuntos Acadêmicos", font=("Segoe UI", 16)).pack()
        
        ctk.CTkFrame(self.frame_login, height=2, fg_color="transparent").pack(fill=tk.X, padx=20, pady=30)
        
        ctk.CTkLabel(self.frame_login, text="Nome do Detetive (Login/Registro):", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=20)
        self.nome_entry = ctk.CTkEntry(self.frame_login, width=400, font=("Segoe UI", 14), placeholder_text="Seu nome de detetive", corner_radius=8)
        self.nome_entry.pack(pady=10, padx=20)
        
        ctk.CTkButton(self.frame_login, text="ENTRAR", font=("Segoe UI", 14, "bold"), command=self.handle_login, corner_radius=8, height=35).pack(pady=20, padx=20, fill="x")

    def criar_widgets_casos(self) -> None:
        """Cria os widgets da tela de seleção de casos."""
        ctk.CTkLabel(self.frame_casos, text="Selecione um Caso:", font=("Segoe UI", 24, "bold")).pack(pady=(10, 20))
        self.caso_selecionado = ctk.StringVar(value=None)
        self.container_lista_casos = ctk.CTkFrame(self.frame_casos, fg_color="transparent")
        self.container_lista_casos.pack(fill="x", padx=100)
        
        ctk.CTkButton(self.frame_casos, text="INICIAR INVESTIGAÇÃO", font=("Segoe UI", 14, "bold"), command=self.iniciar_jogo, corner_radius=8, height=35).pack(pady=30, padx=20, fill="x")
        
        self.widgets_casos: List[ctk.CTkFrame] = []

    def handle_login(self) -> None:
        """Lida com o evento de login, validando o nome e trocando para a tela de seleção de casos."""
        nome = self.nome_entry.get().strip()
        if not nome:
            messagebox.showerror("Erro", "Por favor, insira um nome de detetive.")
            return
            
        self.nome_jogador_atual = nome
        
        if nome not in self.dados_jogadores:
            self.dados_jogadores[nome] = {"casos_concluidos": []}
            self.fm.salvar_dados_jogadores(self.dados_jogadores)
            
        self.frame_login.place_forget()

        self.bg_label.configure(image=self.bg_image_casos)
        
        self.construir_lista_casos()
        self.frame_casos.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    def construir_lista_casos(self) -> None:
        """Constrói a lista de casos disponíveis, marcando os que já foram concluídos."""
        if not self.nome_jogador_atual:
            return

        for widget in self.widgets_casos:
            widget.destroy()
        self.widgets_casos = []
        
        casos_concluidos = self.dados_jogadores.get(self.nome_jogador_atual, {}).get("casos_concluidos", [])
        
        for caso_id, caso_info in self.dados_casos.items():
            status = " (✅ Concluído)" if caso_id in casos_concluidos else " (Pendente)"
            cor_texto = "green" if caso_id in casos_concluidos else "gray80"
            
            titulo_caso = caso_info.get('titulo', 'Caso Desconhecido')
            
            card = ctk.CTkFrame(self.container_lista_casos, corner_radius=8, border_width=2, border_color="gray25")
            card.pack(fill="x", pady=5)
            
            rb = ctk.CTkRadioButton(card, text=f"{titulo_caso}", variable=self.caso_selecionado, value=caso_id, font=("Segoe UI", 16, "bold"))
            rb.pack(anchor="w", padx=15, pady=10)
            
            status_label = ctk.CTkLabel(card, text=status, text_color=cor_texto, font=("Segoe UI", 12))
            status_label.pack(anchor="w", padx=40, pady=(0, 10))
            
            self.widgets_casos.append(card)

    def iniciar_jogo(self) -> None:
        """Inicia o jogo com o caso selecionado."""
        try:
            caso_id = self.caso_selecionado.get()
            
            if not caso_id or caso_id == "None":
                messagebox.showerror("Erro", "Por favor, selecione um caso para iniciar.")
                return

            if not self.nome_jogador_atual:
                messagebox.showerror("Erro", "Ocorreu um erro com o login do jogador.")
                return

            dados_do_caso_selecionado = self.dados_casos[caso_id].copy()
            dados_do_caso_selecionado["id"] = caso_id
            
            self.frame_casos.place_forget()
            
            self.title(f"VERITAS: {dados_do_caso_selecionado['titulo']}")
            
            self.frame_jogo_atual = JogoFrame(self, self.nome_jogador_atual, dados_do_caso_selecionado)
            self.frame_jogo_atual.pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror(
                "Erro ao Carregar Caso",
                f"Não foi possível iniciar o caso.\n\nErro: {e}\n\nCaso ID: {self.caso_selecionado.get()}"
            )
            self.reabrir_menu()
            
    def marcar_caso_concluido(self, caso_id: str) -> None:
        """
        Marca um caso como concluído para o jogador atual.

        Args:
            caso_id (str): O ID do caso a ser marcado como concluído.
        """
        if not self.nome_jogador_atual:
            return

        jogador_data = self.dados_jogadores.get(self.nome_jogador_atual, {"casos_concluidos": []})
        
        if caso_id not in jogador_data["casos_concluidos"]:
            jogador_data["casos_concluidos"].append(caso_id)
            self.dados_jogadores[self.nome_jogador_atual] = jogador_data
            self.fm.salvar_dados_jogadores(self.dados_jogadores)
            
    def reabrir_menu(self) -> None:
        """Fecha a tela do jogo e reabre o menu de seleção de casos."""
        if self.frame_jogo_atual:
            self.frame_jogo_atual.destroy()
            self.frame_jogo_atual = None
            
        self.title("VERITAS - Divisão de Assuntos Acadêmicos")
        
        self.bg_label.configure(image=self.bg_image_casos)
        self.bg_label.lower()

        self.construir_lista_casos()
        
        self.frame_casos.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
