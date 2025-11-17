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
        # Formatado para o novo Textbox
        info = f"--- 📍 {self.nome} ---\n{self.descricao}\n\n"
        if self.pistas:
            info += "🔎 Pistas no local: " + ", ".join([p.nome for p in self.pistas]) + "\n"
        if self.npcs:
            info += "👥 Pessoas presentes: " + ", ".join([n.nome for n in self.npcs]) + "\n"
        
        info += "\n🚪 Saídas: " + ", ".join(self.conexoes.keys())
        return info