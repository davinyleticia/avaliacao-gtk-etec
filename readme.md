# 📝 Sistema de Avaliação ETEC

Este sistema foi desenvolvido para facilitar a aplicação de provas multidisciplinares em ambientes de laboratório, utilizando **Python 3** e **GTK 3**. O foco é a praticidade para o professor e a segurança na integridade das respostas através de criptografia.

### 👩‍🏫 Autora

**Dáviny Letícia Vidal** * **Website:** [vidal.press](https://vidal.press)

* **GitHub:** [@davinyleticia](https://github.com/davinyleticia)
* **Licença:** GNU GPL v3.0

---

## 🚀 Como Funciona?

1. **App Aluno:** O aluno preenche seus dados (Nome e RM), seleciona a disciplina e responde às 10 questões (uma por página com barra de progresso). Ao finalizar, o app gera um **Token Criptografado** (Fernet).
2. **Entrega:** O aluno copia e entrega apenas o código gerado (via formulário, e-mail ou pendrive).
3. **App Professor:** O professor carrega um arquivo CSV contendo os códigos recebidos. O sistema descriptografa, faz a correção automática comparando com o gabarito e gera uma planilha final com **Acertos** e **Menções (MB, B, R, I)**.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**: Linguagem base do projeto.
* **GTK 3 (PyGObject)**: Interface gráfica nativa e leve.
* **Cryptography (Fernet)**: Garante que o aluno não consiga ler ou alterar o código final.
* **Pandas**: Manipulação eficiente de dados e geração de planilhas.
* **PyInstaller**: Ferramenta para transformar os scripts em executáveis independentes.

---

## 📦 Como Gerar os Executáveis

Para que o sistema rode sem a necessidade de instalar o Python em todas as máquinas, gere os binários com os comandos abaixo:

**Executável do Aluno:**

```bash
pyinstaller --noconsole --clean --collect-all gi --collect-all cryptography aluno.py

```

**Executável do Professor:**

```bash
pyinstaller --noconsole --clean --collect-all gi --collect-all pandas professor.py

```

*Os arquivos prontos estarão na pasta `dist/`.*

---

## 🛠 Guia de Customização (Manutenção)

### 1. Onde editar as Perguntas (`aluno.py`)

No arquivo `aluno.py`, localize o dicionário `self.bancos`.

* **p**: O texto da pergunta.
* **opts**: Lista com as opções de resposta.
* **resp**: A resposta correta **exata** (deve ser idêntica a uma das opções).

### 2. Onde editar o Gabarito (`professor.py`)

No arquivo `professor.py`, localize `GABARITOS_MULTIDISCIPLINAR`. As respostas devem estar na mesma ordem das perguntas configuradas no app do aluno.

### 3. Lógica de Menção

A conversão de acertos para menção segue o padrão ETEC em ambos os arquivos na função `calcular_mencao`:

| Acertos | Menção |
| --- | --- |
| 9 - 10 | **MB** |
| 7 - 8 | **B** |
| 5 - 6 | **R** |
| 0 - 4 | **I** |

---

## 💻 Instalação para Desenvolvimento

### Pré-requisitos

* Python 3.10+
* Bibliotecas GTK 3 instaladas (`sudo apt install libgtk-3-dev`)

### Configurar Ambiente Virtual

```bash
# Criar venv com pacotes do sistema (essencial para o GTK/gi)
python3 -m venv --system-site-packages venv

# Ativar ambiente
source venv/bin/activate

# Instalar dependências de processamento e segurança
pip install cryptography pandas

```

---

## 🔒 Segurança Importante

A variável **`CHAVE`** deve ser idêntica em ambos os arquivos. Se a chave for alterada em um deles, o App do Professor não conseguirá descriptografar as respostas geradas pelo Aluno.


## 📚 Dependências e Bibliotecas

O projeto depende de bibliotecas do sistema (Runtime) e bibliotecas do Python. Certifique-se de que todas estejam presentes:

### 1. Dependências do Sistema (Linux/Debian/Ubuntu)

O GTK 3 não é instalado via `pip`, ele é uma biblioteca do sistema operacional.

```bash
sudo apt update
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 libgirepository1.0-dev

```

### 2. Bibliotecas Python (PyPI)

Estas devem ser instaladas dentro do seu ambiente virtual (`venv`):

| Biblioteca | Versão Recomendada | Função no Projeto |
| --- | --- | --- |
| **PyGObject (gi)** | 3.42+ | Interface Gráfica (GTK 3). |
| **Cryptography** | 38.0+ | Criptografia dos resultados (Fernet). |
| **Pandas** | 1.5+ | Manipulação de dados e geração do CSV final. |
| **PyInstaller** | 5.0+ | Criação do executável (.exe ou binário Linux). |

### 3. Instalando via Terminal

Com o ambiente virtual ativo, execute:

```bash
pip install cryptography pandas pyinstaller

```


### ⚠️ Notas de Empacotamento (PyInstaller)

Ao usar o PyInstaller com GTK (`gi`), é obrigatório o uso da flag `--collect-all gi`, pois o Python precisa mapear os arquivos de introspecção do sistema que não estão na pasta padrão do Python.

* **Para o Aluno:** Requer `cryptography` e `gi`.
* **Para o Professor:** Requer `pandas` e `gi`.

## 📄 Licença

Este projeto está sob a licença **GNU GPL v3**. Veja o arquivo [LICENSE](https://www.google.com/search?q=LICENSE) para detalhes.

---

## 👩‍💻 Autora

**Dáviny Letícia Vidal**

* **Email:** [hello@vidal.press](mailto:hello@vidal.press)
* **Website:** [vidal.press](https://vidal.press) | [daviny.dev](https://daviny.dev)
* **LinkedIn:** [linkedin.com/in/davinyleticia](https://linkedin.com/in/davinyleticia)


