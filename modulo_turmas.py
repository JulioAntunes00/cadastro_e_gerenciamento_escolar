from InquirerPy import inquirer
from rich.panel import Panel
from rich.table import Table
import utils

ARQUIVO_TURMAS = "dados/turmas.json"


def carregar_turmas():
    return utils.carregar_dados_json(ARQUIVO_TURMAS)


def salvar_turmas(turmas):
    utils.salvar_dados_json(ARQUIVO_TURMAS, turmas)


def gerenciar_turmas(professor_logado):
    while True:
        utils.limpar_tela()
        utils.console.print(Panel(f"Gerenciamento de Turmas - Professor {professor_logado['nome']}", border_style="blue"))

        escolha = inquirer.select(
            message="Selecione uma opção:",
            choices=[
                "1. Criar nova turma",
                "2. Adicionar aluno à turma",
                "3. Remover aluno da turma",
                "4. Listar minhas turmas",
                "5. Voltar"
            ]
        ).execute()

        if escolha.startswith("1."): criar_turma(professor_logado)
        elif escolha.startswith("2."): adicionar_aluno_turma(professor_logado)
        elif escolha.startswith("3."): remover_aluno_turma(professor_logado)
        elif escolha.startswith("4."): listar_turmas(professor_logado)
        else: break



def criar_turma(professor_logado):
    utils.limpar_tela()
    nome_turma = inquirer.text(message="Nome da nova turma:").execute()
    if not nome_turma:
        utils.console.print("[red]Nome da turma não pode ser vazio.[/red]")
        utils.pausar_tela()
        return

    turmas = carregar_turmas()
    nova_turma = {"nome": nome_turma, "professor": professor_logado["usuario"], "alunos": []}
    turmas.append(nova_turma)
    salvar_turmas(turmas)

    utils.console.print(f"[green]Turma '{nome_turma}' criada com sucesso![/green]")
    utils.pausar_tela()




def adicionar_aluno_turma(professor_logado):
    
    todas_as_turmas = carregar_turmas() 
    
    turmas_professor = [t for t in todas_as_turmas if t["professor"] == professor_logado["usuario"]]
    
    if not turmas_professor:
        utils.console.print("[yellow]Você ainda não possui turmas cadastradas.[/yellow]")
        utils.pausar_tela()
        return

    turma_nome = inquirer.select(
        message="Selecione a turma:", 
        choices=[t["nome"] for t in turmas_professor]
    ).execute()

    usuarios = utils.carregar_dados_json(utils.ARQUIVO_USUARIOS)
    alunos = [u for u in usuarios if u["perfil"] == "Aluno"]
    aluno_login_escolhido = inquirer.select(
        message="Selecione o aluno para adicionar:", 
        choices=[a["usuario"] for a in alunos]
    ).execute()
    
    for turma_existente in todas_as_turmas:
        if aluno_login_escolhido in turma_existente["alunos"]:
            utils.console.print(f"[bold red]Erro:[/bold red] O aluno '{aluno_login_escolhido}' já está na turma '{turma_existente['nome']}'.")
            utils.pausar_tela()
            return
    
    for turma in todas_as_turmas:
        if turma["nome"] == turma_nome and turma["professor"] == professor_logado["usuario"]:
            
            if aluno_login_escolhido not in turma["alunos"]:
                turma["alunos"].append(aluno_login_escolhido)
                utils.console.print(f"[green]Aluno '{aluno_login_escolhido}' adicionado à turma '{turma_nome}'.[/green]")
            else:
                utils.console.print(f"[yellow]Aluno '{aluno_login_escolhido}' já está nessa turma.[/yellow]")
            break
            
    salvar_turmas(todas_as_turmas)
    utils.pausar_tela()


def remover_aluno_turma(professor_logado):
    turmas = carregar_turmas()
    turmas_professor = [t for t in turmas if t["professor"] == professor_logado["usuario"]]

    if not turmas_professor:
        utils.console.print("[yellow]Você ainda não possui turmas cadastradas.[/yellow]")
        utils.pausar_tela()
        return

    turma_nome = inquirer.select(
        message="Selecione a turma:",
        choices=[t["nome"] for t in turmas_professor]
    ).execute()

    turma = next((t for t in turmas_professor if t["nome"] == turma_nome), None)
    if not turma or not turma["alunos"]:
        utils.console.print("[yellow]Nenhum aluno nessa turma para remover.[/yellow]")
        utils.pausar_tela()
        return

    aluno_remover = inquirer.select(
        message="Selecione o aluno para remover:",
        choices=turma["alunos"]
    ).execute()

    confirmado = inquirer.confirm(
        message=f"Tem certeza que deseja remover '{aluno_remover}' da turma '{turma_nome}'?",
        default=False
    ).execute()

    if not confirmado:
        utils.console.print("[cyan]Operação cancelada.[/cyan]")
        utils.pausar_tela()
        return

    turma["alunos"].remove(aluno_remover)

    for t in turmas:
        if t["nome"] == turma_nome and t["professor"] == professor_logado["usuario"]:
            t["alunos"] = turma["alunos"]

    salvar_turmas(turmas)

    utils.console.print(f"[red]Aluno '{aluno_remover}' removido da turma '{turma_nome}'.[/red]")
    utils.pausar_tela()




def listar_turmas(professor_logado):
    turmas = [t for t in carregar_turmas() if t["professor"] == professor_logado["usuario"]]
    utils.limpar_tela()
    utils.console.print(Panel("Suas Turmas", border_style="cyan"))

    if not turmas:
        utils.console.print("Você ainda não criou nenhuma turma.")
    else:
        tabela = Table(
            title="Turmas e Alunos", 
            show_header=True, 
            header_style="bold magenta", 
            show_lines=True
        )
        
        tabela.add_column("Turma", width=15, justify="center")
        tabela.add_column("Alunos", width=50, justify="left") 

        for turma in turmas:
            alunos = ", ".join(turma["alunos"]) if turma["alunos"] else "Nenhum aluno"
            
            tabela.add_row(turma["nome"], alunos)

        utils.console.print(tabela)
    utils.pausar_tela()
    
