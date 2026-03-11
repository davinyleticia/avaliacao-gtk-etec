import gi
import json
from datetime import datetime
from cryptography.fernet import Fernet

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

# Chave de criptografia
CHAVE = b'7P9Xj4kL_8z1nM5vR2uT6aB3cE0gH7iJ9kL2mN5oP8Q='
cipher_suite = Fernet(CHAVE)

class AppAluno(Gtk.Window):
    def __init__(self):
        super().__init__(title="Avaliação ETEC - Vidal Press")
        self.set_default_size(550, 550)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # --- BANCO DE DADOS DE QUESTÕES ---
        # --- BANCO DE DADOS DE QUESTÕES (10 POR DISCIPLINA) ---
        self.bancos = {
            "Desenvolvimento de Sistemas II": [
                {"p": "Qual comando inicia um repositório Git?", "opts": ["git start", "git init", "git new"], "resp": "git init"},
                {"p": "Como salvar alterações no histórico local?", "opts": ["git save", "git commit", "git log"], "resp": "git commit"},
                {"p": "Qual comando envia commits para o servidor remoto?", "opts": ["git push", "git pull", "git send"], "resp": "git push"},
                {"p": "O que o parâmetro '-m' faz no commit?", "opts": ["Move arquivos", "Adiciona mensagem", "Modifica autor"], "resp": "Adiciona mensagem"},
                {"p": "Como verificar o estado atual dos ficheiros?", "opts": ["git status", "git check", "git info"], "resp": "git status"},
                {"p": "Qual comando baixa alterações do remoto?", "opts": ["git get", "git pull", "git download"], "resp": "git pull"},
                {"p": "Para adicionar todos os ficheiros ao stage:", "opts": ["git add .", "git stage all", "git plus"], "resp": "git add ."},
                {"p": "Como ver o histórico de commits?", "opts": ["git history", "git show", "git log"], "resp": "git log"},
                {"p": "O que é o 'Main' ou 'Master'?", "opts": ["Um ficheiro", "A branch principal", "Um comando"], "resp": "A branch principal"},
                {"p": "Como criar uma nova branch?", "opts": ["git branch nome", "git new branch", "git checkout"], "resp": "git branch nome"}
            ],
            "POO (Prog. Orientada a Objetos)": [
                {"p": "O que é uma 'Classe' em POO?", "opts": ["Um objeto vivo", "Um molde/plano", "Uma variável"], "resp": "Um molde/plano"},
                {"p": "Qual pilar permite reutilizar código de outra classe?", "opts": ["Encapsulamento", "Polimorfismo", "Herança"], "resp": "Herança"},
                {"p": "Ocultar dados internos é chamado de:", "opts": ["Abstração", "Encapsulamento", "Instanciação"], "resp": "Encapsulamento"},
                {"p": "O que é um 'Objeto'?", "opts": ["Uma instância de classe", "Um tipo de dado", "Um método"], "resp": "Uma instância de classe"},
                {"p": "Métodos são:", "opts": ["Características", "Ações/Comportamentos", "Nomes de objetos"], "resp": "Ações/Comportamentos"},
                {"p": "Atributos são:", "opts": ["Funções", "Características/Dados", "Eventos"], "resp": "Características/Dados"},
                {"p": "O que é Polimorfismo?", "opts": ["Múltiplas formas", "Esconder código", "Criar cópias"], "resp": "Múltiplas formas"},
                {"p": "Qual modificador permite acesso total?", "opts": ["private", "protected", "public"], "resp": "public"},
                {"p": "O método Construtor serve para:", "opts": ["Destruir objetos", "Inicializar o objeto", "Listar dados"], "resp": "Inicializar o objeto"},
                {"p": "O que é uma Classe Abstrata?", "opts": ["Classe que não vira objeto", "Classe invisível", "Classe sem métodos"], "resp": "Classe que não vira objeto"}
            ],
            "PW I (HTML Básico)": [
                {"p": "Qual tag define o título da aba do browser?", "opts": ["<h1>", "<title>", "<head>"], "resp": "<title>"},
                {"p": "Tag correta para criar um link:", "opts": ["<link>", "<href>", "<a>"], "resp": "<a>"},
                {"p": "Tag para criar uma lista com marcadores (bolinhas):", "opts": ["<ul>", "<ol>", "<li>"], "resp": "<ul>"},
                {"p": "Como inserir uma imagem?", "opts": ["<img src='...'>", "<image href='...'>", "<pic='...'>"], "resp": "<img src='...'>"},
                {"p": "Qual tag define o corpo visível da página?", "opts": ["<head>", "<main>", "<body>"], "resp": "<body>"},
                {"p": "Tag para o maior título da página:", "opts": ["<h6>", "<head>", "<h1>"], "resp": "<h1>"},
                {"p": "Qual atributo define o link de um <a>?", "opts": ["src", "href", "alt"], "resp": "href"},
                {"p": "Tag para quebra de linha:", "opts": ["<br>", "<hr>", "<line>"], "resp": "<br>"},
                {"p": "Para que serve a tag <head>?", "opts": ["Conteúdo visível", "Metadados/Configurações", "Rodapé"], "resp": "Metadados/Configurações"},
                {"p": "Qual tag cria uma tabela?", "opts": ["<tab>", "<grid>", "<table>"], "resp": "<table>"}
            ],
            "PW III (Next.js & DNS)": [
                {"p": "O que faz o serviço DNS?", "opts": ["Cria sites", "Converte nomes em IPs", "Aumenta a RAM"], "resp": "Converte nomes em IPs"},
                {"p": "No Next.js, o que são Componentes?", "opts": ["Peças de UI reutilizáveis", "Drivers", "Servidores"], "resp": "Peças de UI reutilizáveis"},
                {"p": "Qual comando cria um app Next.js?", "opts": ["npx create-next-app", "npm init next", "next build"], "resp": "npx create-next-app"},
                {"p": "Onde ficam as rotas no App Router?", "opts": ["Pasta /src", "Pasta /app", "Pasta /routes"], "resp": "/app"},
                {"p": "O que significa SSR?", "opts": ["Static Site", "Server Side Rendering", "Simple Site Run"], "resp": "Server Side Rendering"},
                {"p": "DNS usa qual porta por padrão?", "opts": ["80", "443", "53"], "resp": "53"},
                {"p": "Como importar um componente no Next.js?", "opts": ["include", "import", "require"], "resp": "import"},
                {"p": "Ficheiro principal de layout no Next.js:", "opts": ["layout.js", "main.js", "index.html"], "resp": "layout.js"},
                {"p": "Qual empresa criou o Next.js?", "opts": ["Google", "Facebook", "Vercel"], "resp": "Vercel"},
                {"p": "O Next.js é baseado em qual biblioteca?", "opts": ["Angular", "Vue", "React"], "resp": "React"}
            ],
            "PAM (Mobile - Expo)": [
                {"p": "O que é o Expo?", "opts": ["Um SO", "Plataforma para React Native", "Um editor de texto"], "resp": "Plataforma para React Native"},
                {"p": "Componente básico para exibir texto no Mobile:", "opts": ["<p>", "<Label>", "<Text>"], "resp": "<Text>"},
                {"p": "Componente que funciona como uma 'div' no mobile:", "opts": ["<View>", "<Box>", "<Area>"], "resp": "<View>"},
                {"p": "Como rodar o projeto Expo no terminal?", "opts": ["npx expo start", "run expo", "npm start app"], "resp": "npx expo start"},
                {"p": "Para lidar com cliques no mobile usamos:", "opts": ["<Button>", "<TouchableOpacity>", "Ambos"], "resp": "Ambos"},
                {"p": "Linguagem principal usada no React Native:", "opts": ["Python", "JavaScript/TypeScript", "Java"], "resp": "JavaScript/TypeScript"},
                {"p": "O que é o 'Hot Reload'?", "opts": ["Reinicia o PC", "Atualiza o app ao salvar", "Limpa o cache"], "resp": "Atualiza o app ao salvar"},
                {"p": "Como estilizar componentes no React Native?", "opts": ["CSS puro", "StyleSheet", "HTML tags"], "resp": "StyleSheet"},
                {"p": "Qual comando instala dependências?", "opts": ["npm add", "npm install", "get library"], "resp": "npm install"},
                {"p": "App para testar o código no telemóvel real:", "opts": ["Expo Go", "Browser", "Simulator"], "resp": "Expo Go"}
            ],
            "Sistemas Operacionais (Linux)": [
                {"p": "Comando para listar arquivos:", "opts": ["ls", "list", "dir"], "resp": "ls"},
                {"p": "Comando para mostrar o caminho atual (diretório):", "opts": ["path", "pwd", "where"], "resp": "pwd"},
                {"p": "Comando para entrar em uma pasta:", "opts": ["go", "cd", "open"], "resp": "cd"},
                {"p": "O comando 'top' serve para:", "opts": ["Ver o topo do arquivo", "Monitorar processos/CPU", "Subir arquivos"], "resp": "Monitorar processos/CPU"},
                {"p": "Como criar uma pasta nova?", "opts": ["newdir", "mkdir", "create"], "resp": "mkdir"},
                {"p": "Comando para remover arquivos:", "opts": ["rm", "del", "remove"], "resp": "rm"},
                {"p": "Como ler o conteúdo de um arquivo no terminal?", "opts": ["read", "cat", "view"], "resp": "cat"},
                {"p": "O que faz o comando 'clear'?", "opts": ["Apaga arquivos", "Limpa a tela", "Fecha o terminal"], "resp": "Limpa a tela"},
                {"p": "Como virar superusuário (root)?", "opts": ["admin", "root", "sudo"], "resp": "sudo"},
                {"p": "Para sair do terminal via comando:", "opts": ["close", "exit", "quit"], "resp": "exit"}
            ]
        }

        self.questoes = []
        self.respostas_selecionadas = []
        self.indice_atual = 0

        self.main_layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(self.main_layout)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.main_layout.pack_start(self.stack, True, True, 0)
        
        # Inicialização das Telas
        self.tela_selecao_disciplina()
        self.tela_cadastro()
        self.tela_questoes_paginada()
        self.tela_finalizacao()
        
        self.criar_footer()
        self.show_all()
        self.connect("destroy", Gtk.main_quit)

    def criar_footer(self):
        # Separador visual
        self.main_layout.pack_start(Gtk.Separator(), False, False, 5)
        
        # Box do Rodapé
        footer_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=5)
        
        lbl_info = Gtk.Label()
        lbl_info.set_markup("<span size='small' color='#555555'>v1.1 ® <b>Dáviny Letícia Vidal</b></span>")
        footer_box.pack_start(lbl_info, False, False, 5)

        # Botão Sobre (Readicionado)
        btn_about = Gtk.Button(label="Sobre")
        btn_about.set_relief(Gtk.ReliefStyle.NONE)
        btn_about.connect("clicked", self.mostrar_sobre)
        footer_box.pack_end(btn_about, False, False, 5)

        self.main_layout.pack_start(footer_box, False, False, 0)

    def mostrar_sobre(self, btn):
        about = Gtk.AboutDialog()
        about.set_transient_for(self)
        about.set_program_name("Sistema de Avaliação GTK")
        about.set_version("1.1")
        about.set_copyright("Copyright © 2026 Dáviny Letícia Vidal")
        about.set_comments("Projeto desenvolvido para as disciplinas lecionadas na ETEC.")
        about.set_website("https://vidal.press")
        about.set_website_label("vidal.press")
        about.set_authors(["Dáviny Letícia Vidal <hello@vidal.press>"])
        about.set_license_type(Gtk.License.GPL_3_0)
        about.run()
        about.destroy()

    # --- TELA 1: SELEÇÃO DE DISCIPLINA ---
    def tela_selecao_disciplina(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20, margin=40)
        lbl = Gtk.Label()
        lbl.set_markup("<span size='large'><b>Selecione a Disciplina</b></span>")
        
        self.combo_disciplinas = Gtk.ComboBoxText()
        for disc in sorted(self.bancos.keys()):
            self.combo_disciplinas.append_text(disc)
        self.combo_disciplinas.set_active(0)

        btn_proximo = Gtk.Button(label="Confirmar e Prosseguir")
        btn_proximo.connect("clicked", self.ao_confirmar_disciplina)

        vbox.pack_start(lbl, False, False, 10)
        vbox.pack_start(self.combo_disciplinas, False, False, 10)
        vbox.pack_start(btn_proximo, False, False, 10)
        self.stack.add_named(vbox, "selecao")

    def ao_confirmar_disciplina(self, btn):
        escolha = self.combo_disciplinas.get_active_text()
        self.questoes = self.bancos[escolha]
        self.respostas_selecionadas = [""] * len(self.questoes)
        self.indice_atual = 0
        self.atualizar_interface_pergunta()
        self.stack.set_visible_child_name("cadastro")

    # --- TELA 2: CADASTRO DO ALUNO ---
    def tela_cadastro(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15, margin=40)
        lbl = Gtk.Label(label="<b>Identificação do Aluno</b>", use_markup=True)
        
        self.ent_nome = Gtk.Entry(placeholder_text="Nome Completo")
        self.ent_rm = Gtk.Entry(placeholder_text="RM (Ex: 12345)")
        
        btn_iniciar = Gtk.Button(label="Iniciar Prova")
        btn_iniciar.connect("clicked", lambda x: self.stack.set_visible_child_name("questoes"))
        
        for w in [lbl, self.ent_nome, self.ent_rm, btn_iniciar]:
            vbox.pack_start(w, False, False, 0)
        self.stack.add_named(vbox, "cadastro")

    # --- TELA 3: QUESTÕES PAGINADAS ---
    def tela_questoes_paginada(self):
        self.vbox_questoes = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20, margin=40)
        self.lbl_pergunta = Gtk.Label(use_markup=True, xalign=0)
        self.lbl_pergunta.set_line_wrap(True)
        
        self.box_opcoes = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        bbox = Gtk.ButtonBox(orientation=Gtk.Orientation.HORIZONTAL, layout_style=Gtk.ButtonBoxStyle.SPREAD)
        self.btn_anterior = Gtk.Button(label="Anterior")
        self.btn_proxima = Gtk.Button(label="Próxima")
        self.btn_anterior.connect("clicked", self.mudar_pergunta, -1)
        self.btn_proxima.connect("clicked", self.mudar_pergunta, 1)
        bbox.add(self.btn_anterior); bbox.add(self.btn_proxima)
        
        self.barra_progresso = Gtk.ProgressBar()
        
        for w in [self.lbl_pergunta, self.box_opcoes, bbox, self.barra_progresso]:
            self.vbox_questoes.pack_start(w, False, False, 5)
        self.stack.add_named(self.vbox_questoes, "questoes")

    def mudar_pergunta(self, btn, direcao):
        self.indice_atual += direcao
        if self.indice_atual >= len(self.questoes):
            self.gerar_token_final()
        else:
            self.atualizar_interface_pergunta()

    def atualizar_interface_pergunta(self):
        if not self.questoes: return
        
        q = self.questoes[self.indice_atual]
        self.lbl_pergunta.set_markup(f"<b>Questão {self.indice_atual + 1} de {len(self.questoes)}</b>\n\n{q['p']}")
        
        for child in self.box_opcoes.get_children():
            child.destroy()
            
        grupo = None
        for opcao in q['opts']:
            rb = Gtk.RadioButton.new_with_label_from_widget(grupo, opcao)
            if grupo is None: grupo = rb
            if self.respostas_selecionadas[self.indice_atual] == opcao:
                rb.set_active(True)
            rb.connect("toggled", self.ao_selecionar, self.indice_atual, opcao)
            self.box_opcoes.pack_start(rb, False, False, 0)
        
        self.btn_anterior.set_sensitive(self.indice_atual > 0)
        self.btn_proxima.set_label("Finalizar" if self.indice_atual == len(self.questoes)-1 else "Próxima")
        self.barra_progresso.set_fraction((self.indice_atual + 1) / len(self.questoes))
        self.show_all()

    def ao_selecionar(self, rb, indice, opcao):
        if rb.get_active():
            self.respostas_selecionadas[indice] = opcao

    # --- TELA 4: FINALIZAÇÃO ---
    def tela_finalizacao(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15, margin=30)
        lbl_instrucao = Gtk.Label(label="<b>Copie o código abaixo e envie ao professor:</b>", use_markup=True)
        
        self.txt_codigo = Gtk.TextView(editable=False, wrap_mode=Gtk.WrapMode.WORD_CHAR)
        sw = Gtk.ScrolledWindow()
        sw.set_min_content_height(150)
        sw.add(self.txt_codigo)
        
        btn_sair = Gtk.Button(label="Fechar Sistema")
        btn_sair.connect("clicked", Gtk.main_quit)
        
        vbox.pack_start(lbl_instrucao, False, False, 0)
        vbox.pack_start(sw, True, True, 0)
        vbox.pack_start(btn_sair, False, False, 0)
        self.stack.add_named(vbox, "finalizacao")

    def gerar_token_final(self):
        dados = {
            "nome": self.ent_nome.get_text(),
            "rm": self.ent_rm.get_text(), 
            "disciplina": self.combo_disciplinas.get_active_text(),
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "respostas": self.respostas_selecionadas
        }
        token = cipher_suite.encrypt(json.dumps(dados).encode())
        self.txt_codigo.get_buffer().set_text(token.decode())
        self.stack.set_visible_child_name("finalizacao")

if __name__ == "__main__":
    app = AppAluno()
    Gtk.main()
    