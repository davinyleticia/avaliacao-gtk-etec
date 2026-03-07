# 📝 Sistema de Avaliação Criptografado - ETEC

Este projeto consiste em um ecossistema de dois softwares desenvolvidos em **Python** e **GTK 3** para a aplicação e correção automatizada de provas. O foco principal é a integridade dos dados através de criptografia simétrica.

## 🚀 Como Funciona?

1. **App Aluno:** O aluno preenche seus dados, seleciona a disciplina e responde às 10 questões (paginadas). Ao finalizar, o app gera um **Token Criptografado** (Fernet).
2. **Entrega:** O aluno entrega apenas o código gerado.
3. **App Professor:** O professor carrega um CSV contendo os nomes e códigos, e o sistema descriptografa, corrige e gera uma planilha final com **Acertos** e **Menções (MB, B, R, I)**.

## 🛠️ Tecnologias Utilizadas

* **Interface Gráfica:** PyGObject (GTK 3)
* **Criptografia:** `cryptography` (Fernet)
* **Manipulação de Dados:** `pandas`
* **Paginamento de Telas:** `Gtk.Stack` e `Gtk.Box`

## 📦 Instalação e Requisitos

### Pré-requisitos

* Python 3.10 ou superior.
* Bibliotecas GTK 3 instaladas no sistema (Runtime).

### Instalar dependências

python3 -m venv --system-site-packages venv

source venv/bin/activate


```bash
pip install pandas cryptography pyGObject

```

## 🔨 Compilação (Gerar .exe)

Para gerar os executáveis com ícone personalizado e sem o console do terminal aparecendo:

**App Aluno:**

```bash
pyinstaller --noconsole --clean --collect-all gi --icon=vidal.ico app_aluno.py

```

**App Professor:**

```bash
pyinstaller --noconsole --clean --collect-all gi --collect-all pandas --icon=vidal.ico app_professor.py

```

```bash

pyinstaller --noconsole --onefile aluno.py

pyinstaller --noconsole --clean --collect-all gi --collect-all cryptography aluno.py

pyinstaller --noconsole --clean --collect-all gi --collect-all pandas professor.py

```

## 🔐 Segurança

O sistema utiliza a biblioteca `cryptography.fernet` para garantir que:

* As respostas não sejam alteradas pelo aluno após a geração do código.
* Apenas o professor (detentor da chave) consiga ler o conteúdo do token.
* Dados sensíveis como Nome, RM e Disciplina fiquem protegidos.

## 📄 Licença

Este projeto está sob a licença **GNU GPL v3**. Veja o arquivo [LICENSE](https://www.google.com/search?q=LICENSE) para detalhes.

---

## 👩‍💻 Autora

**Dáviny Letícia Vidal**

* **Email:** [hello@vidal.press](mailto:hello@vidal.press)
* **Website:** [vidal.press](https://vidal.press) | [daviny.dev](https://daviny.dev)
* **LinkedIn:** [linkedin.com/in/davinyleticia](https://linkedin.com/in/davinyleticia)


