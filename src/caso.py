from typing import Dict, Any
from src.jogo.detetive import Detetive
from src.jogo.personagens.suspeito import Suspeito
from src.jogo.personagens.testemunha import Testemunha
from src.jogo.local import Local
from src.jogo.pistas.pista import Pista
from src.jogo.personagens.npc import NPC
from src.jogo.pistas.pista_fisica import PistaFisica
from src.jogo.pistas.pista_verbal import PistaVerbal
from src.jogo.pistas.pista_documental import PistaDocumental

class Caso:
    """Representa a lógica central de um caso, carregando e conectando todos os elementos do jogo."""

    def __init__(self, nome_detetive: str, dados_caso: Dict[str, Any]) -> None:
        """
        Inicializa um objeto Caso.

        Args:
            nome_detetive (str): O nome do detetive que está jogando.
            dados_caso (Dict[str, Any]): O dicionário com todos os dados do caso, carregado do JSON.
        """
        self.detetive: Detetive = Detetive(nome_detetive)
        self.culpado_id: str = dados_caso["culpado_id"]
        
        self.objetos_locais: Dict[str, Local] = {}
        self.objetos_npcs: Dict[str, NPC] = {}
        self.objetos_pistas: Dict[str, Pista] = {}

        self.carregar_cenario_de_json(dados_caso)

    def carregar_cenario_de_json(self, dados_caso: Dict[str, Any]) -> None:
        """
        Carrega e constrói o cenário do jogo (pistas, NPCs, locais) a partir de um dicionário.

        Args:
            dados_caso (Dict[str, Any]): O dicionário com os dados do caso.

        Raises:
            ValueError: Se o local inicial definido no JSON for inválido.
        """
        
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
            
        # 4. Conectar os Locais e adicionar NPCs/Pistas
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
        local_inicial_id = dados_caso.get("local_inicial")
        self.detetive.local_atual = self.objetos_locais.get(local_inicial_id)
        
        if self.detetive.local_atual is None:
            raise ValueError(f"Local inicial '{local_inicial_id}' não encontrado ou inválido no JSON!")
