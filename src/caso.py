from src.jogo.detetive import Detetive
from src.jogo.personagens.suspeito import Suspeito
from src.jogo.personagens.testemunha import Testemunha
from src.jogo.local import Local
from src.jogo.pistas.pista_fisica import PistaFisica
from src.jogo.pistas.pista_verbal import PistaVerbal
from src.jogo.pistas.pista_documental import PistaDocumental

class Caso:
    def __init__(self, nome_detetive, dados_caso):
        self.detetive = Detetive(nome_detetive)
        self.culpado_id = dados_caso["culpado_id"]
        
        self.objetos_locais = {}
        self.objetos_npcs = {}
        self.objetos_pistas = {}

        self.carregar_cenario_de_json(dados_caso)

    def carregar_cenario_de_json(self, dados_caso):
        
        # 1. Criar todas as Pistas
        for dados_pista in dados_caso["pistas"]:
            pista_obj = None
            tipo = dados_pista["tipo"]
            
            if tipo == "Fisica":
                pista_obj = PistaFisica(dados_pista["nome"], dados_pista["descricao"], dados_pista["local_encontrado"])
            elif tipo == "Verbal":
                pista_obj = PistaVerbal(dados_pista["nome"], dados_pista["descricao"], dados_pista["fonte"])
            elif tipo == "Documental":
                 pista_obj = PistaDocumental(dados_pista["nome"], dados_pista["descricao"], dados_pista["local_encontrado"])

            if pista_obj:
                self.objetos_pistas[dados_pista["id"]] = pista_obj

        # 2. Criar todos os NPCs
        for dados_npc in dados_caso["npcs"]:
            npc_obj = None
            tipo = dados_npc["tipo"]
            pista_associada_obj = None
            
            if "pista_associada" in dados_npc:
                pista_associada_obj = self.objetos_pistas.get(dados_npc["pista_associada"])

            if tipo == "Testemunha":
                npc_obj = Testemunha(dados_npc["nome"], dados_npc["dialogo_inicial"], pista_chave=pista_associada_obj)
            elif tipo == "Suspeito":
                npc_obj = Suspeito(dados_npc["nome"], dados_npc["dialogo_inicial"], dados_npc["culpado"], dados_npc["alibi"])

            if npc_obj:
                self.objetos_npcs[dados_npc["id"]] = npc_obj

        # 3. Criar todos os Locais
        for dados_local in dados_caso["locais"]:
            local_obj = Local(dados_local["nome"], dados_local["descricao"])
            self.objetos_locais[dados_local["id"]] = local_obj
            
        # 4. Conectar os Locais
        for dados_local in dados_caso["locais"]:
            local_atual_obj = self.objetos_locais[dados_local["id"]]

            for direcao, local_id_destino in dados_local["conexoes"].items():
                local_destino_obj = self.objetos_locais.get(local_id_destino)
                if local_destino_obj:
                    local_atual_obj.adicionar_conexao(direcao, local_destino_obj)
                
            for npc_id in dados_local["npcs_presentes"]:
                npc_obj = self.objetos_npcs.get(npc_id)
                if npc_obj:
                    local_atual_obj.npcs.append(npc_obj)
                
            for pista_id in dados_local["pistas_presentes"]:
                pista_obj = self.objetos_pistas.get(pista_id)
                if pista_obj:
                    local_atual_obj.pistas.append(pista_obj)
                
        # 5. Definir ponto de partida
        self.detetive.local_atual = self.objetos_locais.get(dados_caso["local_inicial"])
        
        if self.detetive.local_atual is None:
            raise ValueError(f"Local inicial '{dados_caso.get('local_inicial')}' não encontrado ou inválido no JSON!")
