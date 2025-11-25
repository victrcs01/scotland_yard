import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from src.caso import Caso
from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from interface.interface_menu import InterfaceMenu

class JogoFrame(ctk.CTkFrame):
    """Frame principal da interface do jogo, contendo a tela de informações e ações."""

    def __init__(self, menu_principal: 'InterfaceMenu', nome_detetive: str, dados_caso: Dict[str, Any]) -> None:
        """
        Inicializa o JogoFrame.

        Args:
            menu_principal (InterfaceMenu): A janela principal do menu.
            nome_detetive (str): O nome do jogador.
            dados_caso (Dict[str, Any]): Os dados do caso a ser jogado.
        """
        super().__init__(menu_principal, fg_color="transparent")
        
        try:
            self.menu_principal: 'InterfaceMenu' = menu_principal
            self.caso_id: str = dados_caso["id"]
            
            self.jogo: Caso = Caso(nome_detetive, dados_caso)
            
            self.criar_widgets()
            self.atualizar_ui()
            
        except Exception as e:
            messagebox.showerror(
                "Erro Crítico de Carregamento",
                f"Não foi possível carregar a interface do jogo.\n\n"
                f"Erro: {e}\n\n"
                f"Caso: {dados_caso.get('id', 'DESCONHECIDO')}",
                parent=self.menu_principal
            )
            self.menu_principal.reabrir_menu()

    def criar_widgets(self) -> None:
        """Cria e posiciona todos os widgets da interface do jogo."""
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, minsize=400)
        self.grid_columnconfigure(1, minsize=0)
        
        frame_info = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        frame_info.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")
        frame_info.grid_rowconfigure(1, weight=1)
        frame_info.grid_columnconfigure(0, weight=1)

        self.font_titulo = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        self.font_texto = ctk.CTkFont(family="Segoe UI", size=14)
        self.font_seta = ctk.CTkFont(family="Segoe UI", size=20, weight="bold")
        self.font_menu = ctk.CTkFont(family="Segoe UI", size=12)

        ctk.CTkLabel(frame_info, text="Informações do Local", font=self.font_titulo).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.output_text = ctk.CTkTextbox(frame_info, wrap=tk.WORD, font=self.font_texto, corner_radius=8)
        self.output_text.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.output_text.configure(state=tk.DISABLED)

        frame_acoes = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        frame_acoes.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="nsew")
        frame_acoes.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame_acoes, text="Mover", font=self.font_titulo).grid(row=0, column=0, pady=10, padx=10, sticky="w")
        
        frame_mov_botoes = ctk.CTkFrame(frame_acoes, fg_color="transparent")
        frame_mov_botoes.grid(row=1, column=0, sticky="ew", padx=10)
        frame_mov_botoes.grid_columnconfigure((0, 1, 2), weight=1)

        self.btn_norte = ctk.CTkButton(frame_mov_botoes, text="↑", command=lambda: self.handle_mover("norte"), font=self.font_seta, text_color_disabled="white")
        self.btn_norte.grid(row=0, column=1, padx=2, pady=2, sticky="ew")
        self.btn_oeste = ctk.CTkButton(frame_mov_botoes, text="←", command=lambda: self.handle_mover("oeste"), font=self.font_seta, text_color_disabled="white")
        self.btn_oeste.grid(row=1, column=0, padx=2, pady=2, sticky="ew")
        self.btn_leste = ctk.CTkButton(frame_mov_botoes, text="→", command=lambda: self.handle_mover("leste"), font=self.font_seta, text_color_disabled="white")
        self.btn_leste.grid(row=1, column=2, padx=2, pady=2, sticky="ew")
        self.btn_sul = ctk.CTkButton(frame_mov_botoes, text="↓", command=lambda: self.handle_mover("sul"), font=self.font_seta, text_color_disabled="white")
        self.btn_sul.grid(row=2, column=1, padx=2, pady=2, sticky="ew")

        self.cor_btn_normal = self.btn_norte.cget("fg_color")
        self.cor_btn_desabilitado = "gray40"

        ctk.CTkLabel(frame_acoes, text="Interagir", font=self.font_titulo).grid(row=2, column=0, pady=(20, 10), padx=10, sticky="w")
        ctk.CTkButton(frame_acoes, text="Olhar/Investigar", command=self.handle_olhar).grid(row=3, column=0, sticky="ew", padx=10, pady=2)
        ctk.CTkButton(frame_acoes, text="Ver Caderno", command=self.handle_caderno).grid(row=4, column=0, sticky="ew", padx=10, pady=2)

        self.anotacao_entry = ctk.CTkEntry(frame_acoes, placeholder_text="Escreva sua anotação aqui...", font=self.font_menu)
        self.anotacao_entry.grid(row=5, column=0, sticky="ew", padx=10, pady=(10, 2))
        ctk.CTkButton(frame_acoes, text="Fazer Anotação", command=self.handle_anotacao).grid(row=6, column=0, sticky="ew", padx=10, pady=(0, 4))

        ctk.CTkLabel(frame_acoes, text="Falar / Acusar", font=self.font_titulo).grid(row=7, column=0, pady=(20, 10), padx=10, sticky="w")
        self.npc_option_menu = ctk.CTkOptionMenu(frame_acoes, font=self.font_menu, values=[])
        self.npc_option_menu.grid(row=8, column=0, sticky="ew", padx=10, pady=4)
        
        frame_botoes_falar = ctk.CTkFrame(frame_acoes, fg_color="transparent")
        frame_botoes_falar.grid(row=9, column=0, sticky="ew", padx=10, pady=4)
        frame_botoes_falar.grid_columnconfigure((0,1), weight=1)
        
        ctk.CTkButton(frame_botoes_falar, text="Falar", command=self.handle_falar).grid(row=0, column=0, padx=(0, 2), sticky="ew")
        ctk.CTkButton(frame_botoes_falar, text="Acusar", command=self.handle_acusar, fg_color="#A50000", hover_color="#C00000").grid(row=0, column=1, padx=(2, 0), sticky="ew")

    def print_na_tela(self, mensagem: str) -> None:
        """
        Exibe uma mensagem na caixa de texto de informações.

        Args:
            mensagem (str): A mensagem a ser exibida.
        """
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.insert(tk.END, mensagem + "\n")
        self.output_text.see(tk.END)
        self.output_text.configure(state=tk.DISABLED)

    def atualizar_ui(self) -> None:
        """Atualiza a interface do usuário com as informações do estado atual do jogo."""
        if not self.jogo.detetive.local_atual:
            return

        local_info = self.jogo.detetive.local_atual.get_info()
        
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", local_info)
        self.output_text.configure(state=tk.DISABLED)

        conexoes = self.jogo.detetive.local_atual.conexoes
        
        self.btn_norte.configure(state=tk.NORMAL if "norte" in conexoes else tk.DISABLED, fg_color=self.cor_btn_normal if "norte" in conexoes else self.cor_btn_desabilitado)
        self.btn_sul.configure(state=tk.NORMAL if "sul" in conexoes else tk.DISABLED, fg_color=self.cor_btn_normal if "sul" in conexoes else self.cor_btn_desabilitado)
        self.btn_leste.configure(state=tk.NORMAL if "leste" in conexoes else tk.DISABLED, fg_color=self.cor_btn_normal if "leste" in conexoes else self.cor_btn_desabilitado)
        self.btn_oeste.configure(state=tk.NORMAL if "oeste" in conexoes else tk.DISABLED, fg_color=self.cor_btn_normal if "oeste" in conexoes else self.cor_btn_desabilitado)

        npcs_no_local = [npc.nome for npc in self.jogo.detetive.local_atual.npcs]
        if npcs_no_local:
            self.npc_option_menu.configure(values=npcs_no_local, state=tk.NORMAL)
            self.npc_option_menu.set(npcs_no_local[0])
        else:
            self.npc_option_menu.configure(values=["Nenhum NPC aqui"], state=tk.DISABLED)
            self.npc_option_menu.set("Nenhum NPC aqui")

    def handle_mover(self, direcao: str) -> None:
        """Lida com o evento de clique no botão de movimento."""
        sucesso, msg = self.jogo.detetive.mover(direcao)
        if sucesso and self.jogo.detetive.local_atual:
            self.atualizar_ui()
            self.print_na_tela(f"\n>> Você se moveu para {self.jogo.detetive.local_atual.nome}.")
        
    def handle_olhar(self) -> None:
        """Lida com o evento de clique no botão de investigar."""
        msg = self.jogo.detetive.investigar()
        self.print_na_tela(f"\n>> {msg}")

    def handle_anotacao(self) -> None:
        """Lida com o evento de clique no botão de fazer anotação."""
        texto_anotacao = self.anotacao_entry.get()
        msg = self.jogo.detetive.fazer_anotacao(texto_anotacao)
        self.print_na_tela(f"\n>> {msg}")
        self.anotacao_entry.delete(0, tk.END)

    def handle_caderno(self) -> None:
        """Lida com o evento de clique no botão de ver o caderno."""
        info_caderno = self.jogo.detetive.get_inventario_formatado()
        messagebox.showinfo("Caderno de Anotações", info_caderno)

    def handle_falar(self) -> None:
        """Lida com o evento de clique no botão de falar com NPC."""
        nome_npc = self.npc_option_menu.get()
        msg = self.jogo.detetive.falar_com_npc(nome_npc)
        self.print_na_tela(f"\n>> {msg}")

    def handle_acusar(self) -> None:
        """Lida com o evento de clique no botão de acusar NPC."""
        nome_npc = self.npc_option_menu.get()
        vitoria, msg = self.jogo.detetive.acusar_npc(nome_npc)
        
        self.print_na_tela(f"\n>> {msg}")
        
        if vitoria is not None:
            if vitoria:
                self.menu_principal.marcar_caso_concluido(self.caso_id)
                messagebox.showinfo("Vitória!", "PARABÉNS! CASO ENCERRADO!")
            else:
                messagebox.showerror("Derrota", "ACUSAÇÃO FALHA! O caso esfriou.")
            
            self.fechar_e_reabrir_menu()

    def fechar_e_reabrir_menu(self) -> None:
        """Fecha o frame do jogo e reabre o menu principal."""
        self.menu_principal.reabrir_menu()
