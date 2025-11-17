import customtkinter as ctk 
import tkinter as tk
from tkinter import messagebox

from interface.utils.file_manager import fileManager
from interface.interface_jogo import JogoFrame

class InterfaceMenu(ctk.CTk): # Herda de ctk.CTk
    def __init__(self):
        super().__init__()
        self.title("VERITAS - Divisão de Assuntos Acadêmicos")
        self.geometry("1280x720")
        self.resizable(False, False) # Impede o redimensionamento
        
        # Define a aparência inicial (Dark Mode, tema Blue)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Carregamento dos Dados ---
        self.fm = fileManager()
        dados_brutos_casos = self.fm.carregar_dados_casos()

        # Verifica se os casos foram carregados corretamente
        if not dados_brutos_casos.get("casos"):
            messagebox.showerror("Erro Fatal", "Nenhum caso foi encontrado. Verifique o 'data.json'.")
        else:
            self.dados_casos = dados_brutos_casos.get("casos", {})
            self.dados_jogadores = self.fm.carregar_dados_jogadores()
            self.nome_jogador_atual = None
            
            self.frame_jogo_atual = None

            # --- Carregamento das Imagens de Fundo ---
            try:
                # Usa a classe fileManager para lidar com carregamento de arquivos
                original_image, blurred_image = self.fm.carregar_imagens_bg()
                # Imagem normal para o login
                self.bg_image_login = ctk.CTkImage(original_image, size=(1280, 720))
                # Imagem desfocada para a seleção de casos
                self.bg_image_casos = ctk.CTkImage(blurred_image, size=(1280, 720))
            except FileNotFoundError:
                self.bg_image_login = self.bg_image_casos = None # Lida com a ausência da imagem

            self.bg_label = ctk.CTkLabel(self, text="", image=self.bg_image_login)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_label.lower() # Garante que a imagem fique no fundo
            
            # --- Widgets do Menu ---
            self.frame_login = ctk.CTkFrame(self, fg_color="transparent")
            self.frame_casos = ctk.CTkFrame(self, fg_color="transparent")
            
            self.criar_widgets_login()
            self.criar_widgets_casos()
            
            # Começa mostrando o login (agora sobre a imagem)
            self.frame_login.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def criar_widgets_login(self):
        ctk.CTkLabel(self.frame_login, text="VERITAS", font=("Segoe UI", 32, "bold")).pack(pady=(20, 10))
        ctk.CTkLabel(self.frame_login, text="Divisão de Assuntos Acadêmicos", font=("Segoe UI", 16)).pack()
        
        # Separador
        ctk.CTkFrame(self.frame_login, height=2, fg_color="transparent").pack(fill=tk.X, padx=20, pady=30)
        
        ctk.CTkLabel(self.frame_login, text="Nome do Detetive (Login/Registro):", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=20)
        self.nome_entry = ctk.CTkEntry(self.frame_login, width=400, font=("Segoe UI", 14), placeholder_text="Seu nome de detetive", corner_radius=8)
        self.nome_entry.pack(pady=10, padx=20)
        
        ctk.CTkButton(self.frame_login, text="ENTRAR", font=("Segoe UI", 14, "bold"), command=self.handle_login, corner_radius=8, height=35).pack(pady=20, padx=20, fill="x")

    def criar_widgets_casos(self):
        ctk.CTkLabel(self.frame_casos, text="Selecione um Caso:", font=("Segoe UI", 24, "bold")).pack(pady=(10, 20))
        self.caso_selecionado = ctk.StringVar(value=None)
        self.container_lista_casos = ctk.CTkFrame(self.frame_casos, fg_color="transparent")
        self.container_lista_casos.pack(fill="x", padx=100)
        
        ctk.CTkButton(self.frame_casos, text="INICIAR INVESTIGAÇÃO", font=("Segoe UI", 14, "bold"), command=self.iniciar_jogo, corner_radius=8, height=35).pack(pady=30, padx=20, fill="x")
        
        self.widgets_casos = []

    def handle_login(self):
        nome = self.nome_entry.get().strip()
        if not nome:
            messagebox.showerror("Erro", "Por favor, insira um nome de detetive.")
            return
            
        self.nome_jogador_atual = nome
        
        if nome not in self.dados_jogadores:
            self.dados_jogadores[nome] = {"casos_concluidos": []}
            self.fm.salvar_dados_jogadores(self.dados_jogadores)
            
        self.frame_login.pack_forget()

        # Troca a imagem de fundo para a versão desfocada
        self.bg_label.configure(image=self.bg_image_casos)
        
        self.construir_lista_casos()
        self.frame_casos.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    def construir_lista_casos(self):
        for widget in self.widgets_casos:
            widget.destroy()
        self.widgets_casos = []
        
        casos_concluidos = self.dados_jogadores[self.nome_jogador_atual].get("casos_concluidos", [])
        
        for caso_id, caso_info in self.dados_casos.items():
            
            if caso_id in casos_concluidos:
                status = " (✅ Concluído)"
                cor_texto = "green"
            else:
                status = " (Pendente)"
                cor_texto = "gray80"
                
            titulo_caso = caso_info.get('titulo', 'Caso Desconhecido')
            dificuldade = caso_info.get('dificuldade', 'Normal')
            
            # Cria um "Card" para o RadioButton
            card = ctk.CTkFrame(self.container_lista_casos, corner_radius=8, border_width=2, border_color="gray25")
            card.pack(fill="x", pady=5)
            
            rb = ctk.CTkRadioButton(card, 
                                    text=f"{titulo_caso}", 
                                    variable=self.caso_selecionado, 
                                    value=caso_id, 
                                    font=("Segoe UI", 16, "bold"))
            rb.pack(anchor="w", padx=15, pady=10)
            
            # Adiciona o status
            status_label = ctk.CTkLabel(card, text=status, text_color=cor_texto, font=("Segoe UI", 12))
            status_label.pack(anchor="w", padx=40, pady=(0, 10)) # Indentado sob o radio
            
            self.widgets_casos.append(card) # Adiciona o card para destruição

    def iniciar_jogo(self):
        try:
            caso_id = self.caso_selecionado.get()
            
            if not caso_id or caso_id == "None":
                messagebox.showerror("Erro", "Por favor, selecione um caso para iniciar.")
                return
                
            dados_do_caso_selecionado = self.dados_casos[caso_id].copy()
            dados_do_caso_selecionado["id"] = caso_id
            
            self.frame_casos.pack_forget()
            
            self.title(f"VERITAS: {dados_do_caso_selecionado['titulo']}")
            self.geometry("1280x720") # Janela maior para o jogo
            
            self.frame_jogo_atual = JogoFrame(self, self.nome_jogador_atual, dados_do_caso_selecionado)
            self.frame_jogo_atual.pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror(
                "Erro ao Carregar Caso",
                f"Não foi possível iniciar o caso.\n\n"
                f"Erro: {e}\n\n"
                f"Caso ID: {caso_id}"
            )
            self.reabrir_menu()
            
    def marcar_caso_concluido(self, caso_id):
        jogador_data = self.dados_jogadores.get(self.nome_jogador_atual, {"casos_concluidos": []})
        
        if caso_id not in jogador_data["casos_concluidos"]:
            jogador_data["casos_concluidos"].append(caso_id)
            self.dados_jogadores[self.nome_jogador_atual] = jogador_data
            self.fm.salvar_dados_jogadores(self.dados_jogadores)
            
    def reabrir_menu(self):
        if self.frame_jogo_atual:
            self.frame_jogo_atual.destroy()
            self.frame_jogo_atual = None
            
        self.title("VERITAS - Divisão de Assuntos Acadêmicos")
        self.geometry("1280x720") # Retorna ao tamanho do menu
        
        # Recoloca o label de fundo com a imagem correta (desfocada)
        # Não é mais necessário esconder e reexibir, mas garantimos a imagem certa
        self.bg_label.configure(image=self.bg_image_casos)
        self.bg_label.lower()

        self.construir_lista_casos()
        
        self.frame_casos.place(relx=0.5, rely=0.5, anchor=tk.CENTER)