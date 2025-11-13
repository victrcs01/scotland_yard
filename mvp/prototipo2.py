import tkinter as tk
from tkinter import messagebox, simpledialog

# ==========================================
# 1. AS CLASSES DE LÓGICA DO JOGO (POO)
# (COLE AQUI EXATAMENTE AS MESMAS CLASSES do MVP anterior)
# Pista, PistaFisica, PistaVerbal, NPC, Testemunha, Suspeito, Local, Detetive
# ...
# (Vou incluir apenas a classe Detetive e Local para referência,
# mas você precisa de TODAS as classes de lógica)
# ==========================================

class Pista:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

    def examinar(self):
        return f"Pista: {self.nome}\nDetalhe: {self.descricao}"

class PistaFisica(Pista):
    def __init__(self, nome, descricao, local_encontrado):
        super().__init__(nome, descricao)
        self.local_encontrado = local_encontrado

    def examinar(self):
        return f"[OBJETO] {self.nome} (Encontrado em: {self.local_encontrado})\nAnálise: {self.descricao}"

class PistaVerbal(Pista):
    def __init__(self, nome, descricao, testemunha):
        super().__init__(nome, descricao)
        self.testemunha = testemunha

    def examinar(self):
        return f"[DEPOIMENTO] De: {self.testemunha}\nRelato: \"{self.descricao}\""

class NPC:
    def __init__(self, nome, dialogo_inicial):
        self.nome = nome
        self.dialogo_inicial = dialogo_inicial

    def conversar(self, detetive):
        return f"{self.nome} diz: \"{self.dialogo_inicial}\""

class Testemunha(NPC):
    def __init__(self, nome, dialogo_inicial, pista_chave=None):
        super().__init__(nome, dialogo_inicial)
        self.pista_chave = pista_chave
        self.pista_entregue = False

    def conversar(self, detetive):
        dialogo_base = super().conversar(detetive)
        
        if self.pista_chave and not self.pista_entregue:
            detetive.adicionar_pista(self.pista_chave)
            self.pista_entregue = True
            dialogo_base += f"\n👀 {self.nome} te entrega uma anotação discretamente."
        
        return dialogo_base

class Suspeito(NPC):
    def __init__(self, nome, dialogo_inicial, culpado=False, alibi=""):
        super().__init__(nome, dialogo_inicial)
        self.culpado = culpado
        self.alibi = alibi

    def ser_acusado(self):
        if self.culpado:
            return True, f"\n🚨 {self.nome}: 'Tudo bem, fui eu! Eu precisava do dinheiro!'"
        else:
            return False, f"\n😠 {self.nome}: 'Você está louco? Eu estava {self.alibi}!'"

class Local:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao
        self.conexoes = {} 
        self.pistas = []   
        self.npcs = []     

    def adicionar_conexao(self, direcao, local):
        self.conexoes[direcao] = local

    def get_info(self):
        # Retorna uma string formatada para a GUI
        info = f"--- 📍 {self.nome} ---\n{self.descricao}\n\n"
        if self.pistas:
            info += "🔎 Você vê algo interessante aqui: " + ", ".join([p.nome for p in self.pistas]) + "\n"
        if self.npcs:
            info += "👥 Pessoas presentes: " + ", ".join([n.nome for n in self.npcs]) + "\n"
        
        info += "🚪 Saídas: " + ", ".join(self.conexoes.keys())
        return info

class Detetive:
    def __init__(self, nome):
        self.nome = nome
        self.local_atual = None
        self.inventario = []

    def mover(self, direcao):
        if direcao in self.local_atual.conexoes:
            self.local_atual = self.local_atual.conexoes[direcao]
            return True, f"Você viajou para: {self.local_atual.nome}"
        else:
            return False, "🚫 Não há passagem para essa direção."

    def investigar(self):
        if not self.local_atual.pistas:
            return "Não há nada óbvio para investigar aqui."

        pista = self.local_atual.pistas.pop(0) 
        self.adicionar_pista(pista)
        return f"Você coletou: {pista.nome}\n📝 Nova pista adicionada ao caderno."

    def adicionar_pista(self, pista):
        self.inventario.append(pista)
        
    def falar_com_npc(self, nome_npc):
        if not nome_npc:
            return "Com quem você quer falar? (Digite o nome no campo)"
            
        npc_alvo = next((n for n in self.local_atual.npcs if n.nome.lower() == nome_npc.lower()), None)
        
        if npc_alvo:
            return npc_alvo.conversar(self)
        else:
            return "Essa pessoa não está aqui."

    def acusar_npc(self, nome_npc):
        if not nome_npc:
            return None, "Quem você quer acusar? (Digite o nome no campo)"

        npc_alvo = next((n for n in self.local_atual.npcs if n.nome.lower() == nome_npc.lower()), None)
        
        if npc_alvo and isinstance(npc_alvo, Suspeito):
            vitoria, mensagem = npc_alvo.ser_acusado()
            return vitoria, mensagem
        elif npc_alvo:
            return None, f"{npc_alvo.nome} é apenas uma testemunha, não faz sentido acusá-lo."
        else:
            return None, "Essa pessoa não está aqui."

    def get_inventario_formatado(self):
        if not self.inventario:
            return "Seu caderno de anotações está vazio."
            
        texto_inventario = "📒 --- SEU CADERNO DE ANOTAÇÕES ---\n\n"
        for i, pista in enumerate(self.inventario):
            texto_inventario += f"{i+1}. {pista.examinar()}\n" + ("-"*20) + "\n"
        return texto_inventario


# ==========================================
# 2. LÓGICA DO CASO (Configuração)
# ==========================================

class Caso:
    """Classe que APENAS configura a lógica do caso."""
    def __init__(self):
        self.detetive = Detetive("Sherlock Python")
        self.configurar_cenario()

    def configurar_cenario(self):
        hall = Local("Hall Principal", "Um saguão luxuoso com piso de mármore.")
        biblioteca = Local("Biblioteca", "Estantes cheias de livros antigos. Cheira a poeira.")
        jardim = Local("Jardim de Inverno", "Muitas plantas e uma fonte desligada.")

        hall.adicionar_conexao("norte", biblioteca)
        hall.adicionar_conexao("leste", jardim)
        biblioteca.adicionar_conexao("sul", hall)
        jardim.adicionar_conexao("oeste", hall)

        pista1 = PistaFisica("Relógio Quebrado", "Parou exatamente às 10:30.", "Biblioteca")
        pista2 = PistaVerbal("Fofoca", "O Jardineiro devia dinheiro ao dono da casa.", "Governanta")

        governanta = Testemunha("Sra. Danvers", "Ah, detetive! É uma tragédia!", pista_chave=pista2)
        jardineiro = Suspeito("Jardineiro Bob", "Eu só cuido das plantas, não sei de nada.", culpado=True)
        mordomo = Suspeito("Mordomo James", "Eu estava polindo a prataria.", culpado=False, alibi="polindo a prataria na cozinha")

        biblioteca.pistas.append(pista1)
        hall.npcs.append(governanta)
        hall.npcs.append(mordomo)
        jardim.npcs.append(jardineiro)

        self.detetive.local_atual = hall

# ==========================================
# 3. CLASSE DA INTERFACE (Tkinter)
# ==========================================

class InterfaceJogo(tk.Tk):
    def __init__(self):
        super().__init__() # Inicializa a janela principal do Tkinter
        
        self.jogo = Caso() # Cria a instância do jogo (POO)
        
        self.title("🕵️‍♂️ Mistério do Relógio de Ouro (Tkinter)")
        self.geometry("700x500")

        self.criar_widgets()
        self.atualizar_ui()

    def criar_widgets(self):
        # --- Frame Principal ---
        frame_principal = tk.Frame(self, padx=10, pady=10)
        frame_principal.pack(fill=tk.BOTH, expand=True)

        # --- Frame da Esquerda (Informações) ---
        frame_info = tk.Frame(frame_principal)
        frame_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        tk.Label(frame_info, text="Informações do Local:", font=("Helvetica", 12, "bold")).pack(anchor=tk.W)
        
        # A caixa de texto principal
        self.output_text = tk.Text(frame_info, height=25, width=50, wrap=tk.WORD, font=("Helvetica", 11))
        self.output_text.pack(fill=tk.BOTH, expand=True)
        self.output_text.config(state=tk.DISABLED) # Começa desabilitado para o usuário não digitar

        # --- Frame da Direita (Ações) ---
        frame_acoes = tk.Frame(frame_principal)
        frame_acoes.pack(side=tk.RIGHT, fill=tk.Y, padx=5)

        # Botões de Movimento
        tk.Label(frame_acoes, text="Mover:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W, pady=2)
        self.btn_norte = tk.Button(frame_acoes, text="Norte", width=10, command=lambda: self.handle_mover("norte"))
        self.btn_norte.pack(pady=2)
        
        #... (outros botões de movimento)
        # (Para simplificar o layout, vou colocar todos juntos)
        frame_mov_botoes = tk.Frame(frame_acoes)
        self.btn_oeste = tk.Button(frame_mov_botoes, text="Oeste", width=5, command=lambda: self.handle_mover("oeste"))
        self.btn_oeste.pack(side=tk.LEFT, padx=2)
        self.btn_leste = tk.Button(frame_mov_botoes, text="Leste", width=5, command=lambda: self.handle_mover("leste"))
        self.btn_leste.pack(side=tk.RIGHT, padx=2)
        frame_mov_botoes.pack()
        
        self.btn_sul = tk.Button(frame_acoes, text="Sul", width=10, command=lambda: self.handle_mover("sul"))
        self.btn_sul.pack(pady=2)

        # Botões de Ação
        tk.Label(frame_acoes, text="Interagir:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W, pady=(10, 2))
        tk.Button(frame_acoes, text="Olhar/Investigar", width=15, command=self.handle_olhar).pack(pady=2)
        tk.Button(frame_acoes, text="Ver Caderno", width=15, command=self.handle_caderno).pack(pady=2)

        # Ações com NPC
        tk.Label(frame_acoes, text="Falar / Acusar:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W, pady=(10, 2))
        self.npc_entry = tk.Entry(frame_acoes, width=18)
        self.npc_entry.pack(pady=2)
        tk.Button(frame_acoes, text="Falar", width=15, command=self.handle_falar).pack(pady=2)
        tk.Button(frame_acoes, text="Acusar", width=15, command=self.handle_acusar, bg="red", fg="white").pack(pady=2)

    def print_na_tela(self, mensagem):
        """Helper para escrever na caixa de texto"""
        self.output_text.config(state=tk.NORMAL) # Habilita para escrever
        self.output_text.insert(tk.END, mensagem + "\n")
        self.output_text.see(tk.END) # Rola para o final
        self.output_text.config(state=tk.DISABLED) # Desabilita de novo

    def atualizar_ui(self):
        """Atualiza a tela com as informações do local atual."""
        local_info = self.jogo.detetive.local_atual.get_info()
        
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END) # Limpa a tela
        self.output_text.insert("1.0", local_info) # Insere info do local
        self.output_text.config(state=tk.DISABLED)

        # Atualiza estado dos botões de direção
        conexoes = self.jogo.detetive.local_atual.conexoes
        self.btn_norte.config(state=tk.NORMAL if "norte" in conexoes else tk.DISABLED)
        self.btn_sul.config(state=tk.NORMAL if "sul" in conexoes else tk.DISABLED)
        self.btn_leste.config(state=tk.NORMAL if "leste" in conexoes else tk.DISABLED)
        self.btn_oeste.config(state=tk.NORMAL if "oeste" in conexoes else tk.DISABLED)

    # --- Handlers de Eventos (O que os botões fazem) ---

    def handle_mover(self, direcao):
        sucesso, msg = self.jogo.detetive.mover(direcao)
        if sucesso:
            self.atualizar_ui()
            self.print_na_tela("\n>> Você se moveu.")
        
    def handle_olhar(self):
        msg = self.jogo.detetive.investigar()
        self.print_na_tela(f"\n>> {msg}")

    def handle_caderno(self):
        info_caderno = self.jogo.detetive.get_inventario_formatado()
        # Mostra o caderno em uma janela pop-up
        messagebox.showinfo("Caderno de Anotações", info_caderno)

    def handle_falar(self):
        nome_npc = self.npc_entry.get()
        msg = self.jogo.detetive.falar_com_npc(nome_npc)
        self.print_na_tela(f"\n>> {msg}")
        self.npc_entry.delete(0, tk.END) # Limpa o campo

    def handle_acusar(self):
        nome_npc = self.npc_entry.get()
        vitoria, msg = self.jogo.detetive.acusar_npc(nome_npc)
        
        self.print_na_tela(f"\n>> {msg}")
        self.npc_entry.delete(0, tk.END) # Limpa o campo
        
        if vitoria is not None: # Jogo acabou (Vitória ou Derrota)
            if vitoria:
                messagebox.showinfo("Fim de Jogo!", "PARABÉNS! CASO ENCERRADO!")
            else:
                messagebox.showerror("Fim de Jogo!", "ACUSAÇÃO FALHA! O caso esfriou.")
            self.destroy() # Fecha a janela principal


# ==========================================
# 4. EXECUTAR O JOGO
# ==========================================

if __name__ == "__main__":
    app = InterfaceJogo()
    app.mainloop() # Inicia o loop de eventos do Tkinter