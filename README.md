# VERITAS - Divisão de Assuntos Acadêmicos

VERITAS é um jogo de mistério e detetive baseado em texto, onde o jogador assume o papel de um detetive para resolver casos intrigantes. O jogo apresenta uma interface gráfica construída com CustomTkinter e uma narrativa ramificada que se desenrola com base nas ações do jogador.

## Como executar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/veritas.git
   cd veritas
   ```

2. **Instale as dependências:**
   Este projeto requer Python 3 e as seguintes bibliotecas:
   - `customtkinter`
   - `Pillow` (para manipulação de imagem)

   Instale-os usando pip:
   ```bash
   pip install customtkinter pillow
   ```

3. **Execute o jogo:**
   ```bash
   python main.py
   ```

## Diagrama de Classes

```mermaid
classDiagram
    class InterfaceMenu {
        +__init__()
        +criar_widgets_login()
        +criar_widgets_casos()
        +handle_login()
        +construir_lista_casos()
        +iniciar_jogo()
        +marcar_caso_concluido()
        +reabrir_menu()
    }

    class JogoFrame {
        +__init__(menu_principal, nome_detetive, dados_caso)
        +criar_widgets()
        +print_na_tela(mensagem)
        +atualizar_ui()
        +handle_mover(direcao)
        +handle_olhar()
        +handle_anotacao()
        +handle_caderno()
        +handle_falar()
        +handle_acusar()
        +fechar_e_reabrir_menu()
    }

    class Caso {
        +__init__(nome_detetive, dados_caso)
        +carregar_cenario_de_json(dados_caso)
    }

    class Detetive {
        +__init__(nome)
        +mover(direcao)
        +investigar()
        +fazer_anotacao(texto)
        +get_inventario_formatado()
        +falar_com_npc(nome_npc)
        +acusar_npc(nome_npc)
    }

    class Local {
        +__init__(nome, descricao)
        +adicionar_conexao(direcao, local)
        +get_info()
    }

    class Pista {
        +__init__(nome, descricao)
    }
    class PistaFisica {
        +__init__(nome, descricao, local_encontrado)
    }
    class PistaVerbal {
        +__init__(nome, descricao, fonte)
    }
    class PistaDocumental {
        +__init__(nome, descricao, local_encontrado)
    }
    class PistaAnotacao {
        +__init__(texto)
    }

    class NPC {
        +__init__(nome, dialogo_inicial)
    }
    class Testemunha {
        +__init__(nome, dialogo_inicial, pista_chave)
        +falar()
    }
    class Suspeito {
        +__init__(nome, dialogo_inicial, culpado, alibi)
        +falar()
    }

    InterfaceMenu "1" -- "1" JogoFrame : cria
    JogoFrame "1" -- "1" Caso : cria
    Caso "1" -- "1" Detetive : cria
    Caso "1" -- "0..*" Local : cria
    Caso "1" -- "0..*" Pista : cria
    Caso "1" -- "0..*" NPC : cria
    Detetive "1" -- "1" Local : esta_em
    Local "1" -- "0..*" Pista : contem
    Local "1" -- "0..*" NPC : contem

    Pista <|-- PistaFisica
    Pista <|-- PistaVerbal
    Pista <|-- PistaDocumental
    Pista <|-- PistaAnotacao
    NPC <|-- Testemunha
    NPC <|-- Suspeito
```
