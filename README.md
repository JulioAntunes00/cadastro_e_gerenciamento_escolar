# Sistema de Gerenciamento Escolar e Apoio Didático (PIM)

Projeto desenvolvido como parte do Projeto Integrado Multidisciplinar (PIM). O objetivo foi criar uma aplicação em console utilizando Python que simula o ecossistema de uma escola, integrando administração, professores e alunos, com o diferencial de utilizar Inteligência Artificial para suporte ao estudante.

## 📋 Funcionalidades

O sistema possui controle de acesso baseado em níveis de permissão:

###  Coordenador
- **Gerenciar Usuários:** Cadastro de novos professores no sistema.
- **Listagem:** Visualização de todos os usuários cadastrados.

###  Professor
- **Gerenciar Alunos:** Cadastro e listagem de alunos.
- **Gestão de Turmas:**
  - Criação de novas turmas.
  - Inserir alunos em turmas.
  - Remover alunos de turmas.
  - Listar turmas ativas.
- **Material Didático:** Adicionar ou remover conteúdos de estudo para os alunos.

###  Aluno
- **Acesso ao Conteúdo:** Visualização dos materiais disponibilizados pelos professores.
- **Assistente Virtual (IA):** Integração com a API do **Google Gemini**. O aluno pode tirar dúvidas e conversar com a IA diretamente pelo terminal, em tempo real.

---

##  Tecnologias Utilizadas

- **Python 3**: Linguagem principal.
- **Google Generative AI (Gemini API)**: Para o módulo de inteligência artificial.
- **Bibliotecas auxiliares**: Manipulação de arquivos e interface de texto.

---

##  Como rodar o projeto

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/JulioAntunes00/cadastro_e_gerenciamento_escolar.git
   ```
2. **Instale as dependências:** Certifique-se de estar na pasta do projeto e execute:

   ```Bash
    pip install -r requirements.txt
    ```
3. **Configuração da API:** Por questões de segurança, a chave da API não está incluída no repositório.

    Gere sua própria chave no Google AI Studio.
    Abra o arquivo config.py.
    Substitua a chave na variável indicada.
    
4. **Execute o sistema:**

    ```Bash
    python main.py
    ```