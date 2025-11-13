import sys
import time

# ==========================================
# 1. SISTEMA DE PISTAS (Herança e Polimorfismo)
# ==========================================

class Pista:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

    def examinar(self):
        # Método base
        return f"Pista: {self.nome}\nDetalhe: {self.descricao}"

class PistaFisica(Pista):
    def __init__(self, nome, descricao, local_encontrado):
        super().__init__(nome, descricao)
        self.local_encontrado = local_encontrado

    def examinar(self):
        # Polimorfismo: Comportamento específico para objetos físicos
        return f"[OBJETO] {self.nome} (Encontrado em: {self.local_encontrado})\nAnálise: {self.descricao}"

class PistaVerbal(Pista):
    def __init__(self, nome, descricao, testemunha):
        super().__init__(nome, descricao)
        self.testemunha = testemunha

    def examinar(self):
        # Polimorfismo: Comportamento específico para depoimentos
        return f"[DEPOIMENTO] De: {self.testemunha}\nRelato: \"{self.descricao}\""

# ==========================================
# 2. SISTEMA DE PERSONAGENS (Herança)
# ==========================================

class NPC:
    def __init__(self, nome, dialogo_inicial):
        self.nome = nome
        self.dialogo_inicial = dialogo_inicial

    def conversar(self, detetive):
        print(f"\n{self.nome} diz: \"{self.dialogo_inicial}\"")

class Testemunha(NPC):
    def __init__(self, nome, dialogo_inicial, pista_chave=None):
        super().__init__(nome, dialogo_inicial)
        self.pista_chave = pista_chave
        self.pista_entregue = False

    def conversar(self, detetive):
        super().conversar(detetive) # Chama o método da classe mãe
        
        if self.pista_chave and not self.pista_entregue:
            print(f"👀 {self.nome} te entrega uma anotação discretamente.")
            detetive.adicionar_pista(self.pista_chave)
            self.pista_entregue = True

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

# ==========================================
# 3. AMBIENTE (Composição)
# ==========================================

class Local:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao
        self.conexoes = {} # Ex: {'norte': local_obj}
        self.pistas = []   # Lista de objetos Pista
        self.npcs = []     # Lista de objetos NPC

    def adicionar_conexao(self, direcao, local):
        self.conexoes[direcao] = local

    def entrar(self):
        print(f"\n--- 📍 {self.nome} ---")
        print(self.descricao)
        
        if self.pistas:
            print("🔎 Você vê algo interessante aqui: " + ", ".join([p.nome for p in self.pistas]))
        if self.npcs:
            print("👥 Pessoas presentes: " + ", ".join([n.nome for n in self.npcs]))
        
        print("🚪 Saídas: " + ", ".join(self.conexoes.keys()))

# ==========================================
# 4. JOGADOR (Encapsulamento)
# ==========================================

class Detetive:
    def __init__(self, nome):
        self.nome = nome
        self.local_atual = None
        self.inventario = []

    def mover(self, direcao):
        if direcao in self.local_atual.conexoes:
            self.local_atual = self.local_atual.conexoes[direcao]
            self.local_atual.entrar()
        else:
            print("🚫 Não há passagem para essa direção.")

    def investigar(self):
        if not self.local_atual.pistas:
            print("Não há nada óbvio para investigar aqui.")
            return

        # Pega a primeira pista (simplificação para o MVP)
        pista = self.local_atual.pistas.pop(0) 
        print(f"Você coletou: {pista.nome}")
        self.adicionar_pista(pista)

    def adicionar_pista(self, pista):
        self.inventario.append(pista)
        print(f"📝 Nova pista adicionada ao caderno: {pista.nome}")

    def falar_com_npc(self, nome_npc):
        # Busca NPC pelo nome no local atual
        npc_alvo = next((n for n in self.local_atual.npcs if n.nome.lower() == nome_npc.lower()), None)
        
        if npc_alvo:
            npc_alvo.conversar(self)
        else:
            print("Essa pessoa não está aqui.")

    def acusar_npc(self, nome_npc):
        npc_alvo = next((n for n in self.local_atual.npcs if n.nome.lower() == nome_npc.lower()), None)
        
        if npc_alvo and isinstance(npc_alvo, Suspeito):
            vitoria, mensagem = npc_alvo.ser_acusado()
            print(mensagem)
            return vitoria
        elif npc_alvo:
            print(f"{npc_alvo.nome} é apenas uma testemunha, não faz sentido acusá-lo.")
        else:
            print("Essa pessoa não está aqui.")
        return None

    def ver_inventario(self):
        print("\n📒 --- SEU CADERNO DE ANOTAÇÕES ---")
        if not self.inventario:
            print("Vazio.")
        for i, pista in enumerate(self.inventario):
            print(f"{i+1}. {pista.examinar()}")

# ==========================================
# 5. LOOP DO JOGO (Controller)
# ==========================================

class Caso:
    def __init__(self):
        self.detetive = Detetive("Sherlock Python")
        self.configurar_cenario()

    def configurar_cenario(self):
        # Criar Locais
        hall = Local("Hall Principal", "Um saguão luxuoso com piso de mármore.")
        biblioteca = Local("Biblioteca", "Estantes cheias de livros antigos. Cheira a poeira.")
        jardim = Local("Jardim de Inverno", "Muitas plantas e uma fonte desligada.")

        # Conectar Locais
        hall.adicionar_conexao("norte", biblioteca)
        hall.adicionar_conexao("leste", jardim)
        biblioteca.adicionar_conexao("sul", hall)
        jardim.adicionar_conexao("oeste", hall)

        # Criar Pistas
        pista1 = PistaFisica("Relógio Quebrado", "Parou exatamente às 10:30.", "Biblioteca")
        pista2 = PistaVerbal("Fofoca", "O Jardineiro devia dinheiro ao dono da casa.", "Governanta")

        # Criar NPCs
        # A Governanta é testemunha
        governanta = Testemunha("Sra. Danvers", "Ah, detetive! É uma tragédia!", pista_chave=pista2)
        
        # O Jardineiro é o culpado
        jardineiro = Suspeito("Jardineiro Bob", "Eu só cuido das plantas, não sei de nada.", culpado=True)
        
        # O Mordomo é inocente (Red Herring)
        mordomo = Suspeito("Mordomo James", "Eu estava polindo a prataria.", culpado=False, alibi="polindo a prataria na cozinha")

        # Distribuir nos locais
        biblioteca.pistas.append(pista1)
        hall.npcs.append(governanta)
        hall.npcs.append(mordomo)
        jardim.npcs.append(jardineiro)

        # Definir inicio
        self.detetive.local_atual = hall

    def jogar(self):
        print("\n🕵️‍♂️ --- MISTÉRIO DO RELÓGIO DE OURO ---")
        print("Objetivo: Encontre pistas e acuse o culpado (Suspeito).")
        self.detetive.local_atual.entrar()

        while True:
            comando_bruto = input("\nO que fazer? (ir [direcao], olhar, falar [nome], acusar [nome], caderno, sair): ").strip().lower()
            partes = comando_bruto.split()
            acao = partes[0]

            if acao == "sair":
                print("Saindo do caso...")
                break
            
            elif acao == "ir":
                if len(partes) > 1:
                    self.detetive.mover(partes[1])
                else:
                    print("Ir para onde?")

            elif acao == "olhar" or acao == "investigar":
                self.detetive.investigar()

            elif acao == "falar":
                if len(partes) > 1:
                    # Reconstrói o nome caso seja composto (ex: falar Sra. Danvers)
                    nome = " ".join(partes[1:]) 
                    self.detetive.falar_com_npc(nome)
                else:
                    print("Falar com quem?")

            elif acao == "acusar":
                if len(partes) > 1:
                    nome = " ".join(partes[1:])
                    resultado = self.detetive.acusar_npc(nome)
                    if resultado is True:
                        print("\n🏆 PARABÉNS! CASO ENCERRADO! Você pegou o culpado.")
                        break
                    elif resultado is False:
                        print("\n❌ ACUSAÇÃO FALHA! O suspeito provou inocência. O caso esfriou. FIM DE JOGO.")
                        break
                else:
                    print("Acusar quem?")

            elif acao == "caderno":
                self.detetive.ver_inventario()

            else:
                print("Comando inválido.")

if __name__ == "__main__":
    jogo = Caso()
    jogo.jogar()