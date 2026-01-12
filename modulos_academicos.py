from InquirerPy import inquirer
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
import config 
import utils 

import google.generativeai as genai



def acessar_materiais():   
    materiais = utils.carregar_dados_json(utils.ARQUIVO_MATERIAIS)
    
    if not materiais:
        utils.limpar_tela()
        utils.console.print("Nenhum material disponível no momento.")
        utils.pausar_tela()
        return

    opcoes_menu = [m['disciplina'] for m in materiais] + ["Voltar"]
    
    while True:
        utils.limpar_tela()
        utils.console.print(Panel("Material Didático", border_style="green"))
        disciplina_escolhida = inquirer.select(
            message="Selecione a disciplina:",
            choices=opcoes_menu
        ).execute()

        if disciplina_escolhida == "Voltar":
            break

        for material in materiais:
            if material['disciplina'] == disciplina_escolhida:
                utils.limpar_tela()
                utils.console.print(Panel(
                    Text(material['conteudo'], justify="left"),
                    title=f"[bold cyan]{disciplina_escolhida}[/bold cyan]"
                ))
                utils.pausar_tela()
                break


# Função: iniciar_chat_ia
def iniciar_chat_ia():
    utils.limpar_tela()
    utils.console.print(Panel("Assistente Acadêmico (IA Google Gemini)", border_style="magenta"))
    
    # Configuração da API
    try:
        genai.configure(api_key=config.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        chat = model.start_chat(history=[])
        
        utils.console.print("[cyan]Conectado![/cyan] Você pode começar a conversar. Digite 'sair' ou 'fim' para encerrar.")
    except Exception as e:
        utils.console.print(f"[bold red]Erro ao configurar a IA:[/bold red] {e}")
        utils.pausar_tela()
        return

    while True:
        pergunta = inquirer.text(message="Você:").execute()
        if not pergunta: continue

        if any(p in pergunta.lower() for p in ["sair", "tchau", "fim"]):
            utils.console.print("[magenta]Assistente:[/magenta] Até mais! Bons estudos.")
            utils.time.sleep(2)
            break

        spinner = Spinner("dots", text=" Assistente está digitando...")
        with Live(spinner, refresh_per_second=10, transient=True):
            try:
                response = chat.send_message(pergunta)
                resposta_ia = response.text
            
            except Exception as e:
                resposta_ia = f"Ocorreu um erro na comunicação com a IA: {e}"

        utils.console.print(f"[magenta]Assistente:[/magenta] {resposta_ia}")



def adicionar_material():
    utils.limpar_tela()
    utils.console.print(Panel("Gerenciador de Material Didático", border_style="blue"))

    disciplina = inquirer.text(message="Qual o nome da disciplina?").execute()
    conteudo = inquirer.text(
        message="Digite o conteúdo da aula:",
        multiline=True,
        instruction="(Pressione Esc e depois Enter para confirmar)"
    ).execute()

    if not disciplina or not conteudo:
        utils.console.print("\n[red]Operação cancelada. Disciplina e conteúdo não podem ser vazios.[/red]")
        utils.pausar_tela()
        return

    materiais = utils.carregar_dados_json(utils.ARQUIVO_MATERIAIS)
    
    novo_material = {
        "disciplina": disciplina,
        "conteudo": conteudo
    }

    materiais.append(novo_material)
    utils.salvar_dados_json(utils.ARQUIVO_MATERIAIS, materiais)

    utils.console.print(f"\n[green]Material para '{disciplina}' adicionado com sucesso![/green]")
    utils.pausar_tela()


def remover_material():
    utils.limpar_tela()
    utils.console.print(Panel("Remover Material Didático", border_style="red"))

    materiais = utils.carregar_dados_json(utils.ARQUIVO_MATERIAIS)

    if not materiais:
        utils.console.print("\n[yellow]Nenhum material cadastrado para remover.[/yellow]")
        utils.pausar_tela()
        return

    opcoes_disciplinas = [m['disciplina'] for m in materiais] + ["Cancelar"]

    disciplina_a_remover = inquirer.select(
        message="Qual material você deseja remover?",
        choices=opcoes_disciplinas
    ).execute()

    if disciplina_a_remover == "Cancelar":
        return

    confirmado = inquirer.confirm(
        message=f"Tem certeza que deseja remover o material de '{disciplina_a_remover}'?",
        default=False
    ).execute()

    if confirmado:
        novos_materiais = [m for m in materiais if m['disciplina'] != disciplina_a_remover]

        utils.salvar_dados_json(utils.ARQUIVO_MATERIAIS, novos_materiais)

        utils.console.print(f"\n[green]Material de '{disciplina_a_remover}' removido com sucesso![/green]")
    else:
        utils.console.print("\n[yellow]Operação cancelada.[/yellow]")

    utils.pausar_tela()





def gerenciar_materiais():
    while True:
        utils.limpar_tela()
        utils.console.print(Panel("Gerenciador de Material Didático", border_style="blue"))

        escolha = inquirer.select(
            message="O que você deseja fazer?",
            choices=[
                "1. Adicionar novo material",
                "2. Remover material existente",
                "3. Voltar ao menu anterior"
            ],
            default=None
        ).execute()

        if not escolha or escolha.startswith("3."):
            break
        elif escolha.startswith("1."):
            adicionar_material()
        elif escolha.startswith("2."):
            remover_material()
