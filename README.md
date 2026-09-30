# 🚀 Sistema Financeiro Desktop

> Uma aplicação desktop em Python para controle financeiro pessoal e bancário, com projeção de saldos, gráficos interativos e exportação de dados para Excel.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Como Executar o Projeto](#-como-executar-o-projeto)
- [Licença](#-licença)
- [Autores](#-autores)


---

## 💻 Sobre o Projeto

O **Sistema Financeiro Desktop** é um software de gestão financeira criado para facilitar o acompanhamento de contas bancárias, entradas e saídas financeiras. A aplicação permite cadastrar múltiplas contas, registrar movimentações corriqueiras e obter informações relevantes como projeção de saldo até o fim do mês ou datas específicas.

O projeto resolve o problema da falta de previsibilidade financeira através de uma interface moderna, oferecendo gráficos estatísticos integrados para visualização do fluxo de caixa e recurso de exportação direta de histórico para tabelas do Excel.

---

## ✨ Funcionalidades

- 🏦 **Gerenciamento de Contas:** Cadastro e alternância entre múltiplas contas bancárias com saldos iniciais.
- 💳 **Registro de Movimentações:** Cadastro de entradas e saídas financeiras com verificação e padronização de datas (`YYYY-MM-DD`).
- 📈 **Gráficos Financeiros:** Visualização interativa de movimentações mensais e anuais (Total, Entradas ou Saídas) integrada via Matplotlib.
- 🔮 **Previsão de Saldo:** Cálculo automático e projeção de saldo futuro até o fim do mês corrente ou para datas customizadas.
- ✏️ **Edição de Registros:** Atualização dinâmica de registros existentes por ID (alteração de data, fornecedor/devedor, valor ou conta).
- 📊 **Exportação de Dados:** Geração automatizada de relatórios em formato `.xlsx` (Excel) via Pandas.

---

## 🛠️ Tecnologias Utilizadas

As seguintes ferramentas, linguagens e bibliotecas foram usadas na construção do projeto:

- **[Python](https://www.python.org/)** — Linguagem principal do projeto
- **[CustomTkinter](https://customtkinter.tesseract.site/)** — Interface gráfica moderna e personalizável (GUI)
- **[SQLite3](https://www.sqlite.org/)** — Banco de dados relacional embutido
- **[Matplotlib](https://matplotlib.org/)** — Renderização de gráficos financeiros dinâmicos
- **[Pandas](https://pandas.pydata.org/)** — Manipulação de dados e exportação de relatórios para Excel
- **[OpenPyXL](https://openpyxl.readthedocs.io/)** — Suporte para criação e escrita de arquivos `.xlsx`
- **[Tkinter](https://docs.python.org/3/library/tkinter.html)** *(built-in)* — Caixas de diálogo e elementos legados de interface

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas:
- [Git](https://git-scm.com)
- [Python 3.10+](https://www.python.org/)

### 🎲 Passo a Passo

```bash
# 1. Clone este repositório
$ git clone [https://github.com/gtbarros/nome-do-repositorio.git](https://github.com/seu-usuario/nome-do-repositorio.git)

# 2. Acesse a pasta do projeto no terminal
$ cd nome-do-repositorio

# 3. Crie um ambiente virtual (opcional, mas recomendado)
$ python -m venv venv

# Ative o ambiente virtual:
# No Windows:
$ venv\Scripts\activate
# No Linux/Mac:
$ source venv/bin/activate

# 4. Instale as dependências
$ pip install customtkinter matplotlib pandas openpyxl

# 5. Execute a aplicação
$ python main.py

