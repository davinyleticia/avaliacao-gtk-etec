import gi
import json
import webbrowser # Para abrir os links no navegador
from datetime import datetime
from cryptography.fernet import Fernet

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

CHAVE = b'7P9Xj4kL_8z1nM5vR2uT6aB3cE0gH7iJ9kL2mN5oP8Q='
cipher_suite = Fernet(CHAVE)

class AppAluno(Gtk.Window):
    def __init__(self):
        super().__init__(title="Avaliação ETEC - Vidal Press")
        self.set_default_size(550, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        self.main_layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(self.main_layout)

        # Questões (Mesma lista anterior)
        self.questoes = [
            {"p": "Qual comando inicia um repositório Git na pasta?", "opts": ["git start", "git init", "git new"], "resp": "git init"},
            {"p": "Para salvar as alterações no histórico usamos o:", "opts": ["git commit", "git save", "git push"], "resp": "git commit"},
            {"p": "Qual pilar da POO permite que uma classe herde de outra?", "opts": ["Encapsulamento", "Polimorfismo", "Herança"], "resp": "Herança"},
            {"p": "Ocultar detalhes internos e proteger dados é:", "opts": ["Abstração", "Encapsulamento", "Instanciação"], "resp": "Encapsulamento"},
            {"p": "Em POO, um 'plano' ou 'molde' para criar objetos é a:", "opts": ["Classe", "Método", "Atributo"], "resp": "Classe"},
            {"p": "Qual comando é usado para navegar entre pastas (diretórios)?", "opts": ["ls", "mkdir", "cd"], "resp": "cd"},
            {"p": "Para listar os arquivos de uma pasta, usamos o:", "opts": ["ls", "top", "list"], "resp": "ls"},
            {"p": "O comando 'top' no Linux serve para:", "opts": ["Ver processos e CPU", "Subir um arquivo", "Ver o topo do arquivo"], "resp": "Ver processos e CPU"},
            {"p": "Como voltar para a pasta anterior via terminal?", "opts": ["cd ..", "cd back", "back"], "resp": "cd .."},
            {"p": "Qual comando mostra o caminho da pasta atual (Print Working Directory)?", "opts": ["dir", "pwd", "path"], "resp": "pwd"}
        ]
        self.respostas_selecionadas = [""] * len(self.questoes)
        self.indice_atual = 0

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.main_layout.pack_start(self.stack, True, True, 0)
        
        self.tela_cadastro()
        self.tela_questoes_paginada()
        self.tela_finalizacao()
        self.criar_footer() # Rodapé atualizado com botões
        
        self.show_all()
        self.connect("destroy", Gtk.main_quit)

    def criar_footer(self):
        separador = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.main_layout.pack_start(separador, False, False, 5)
        
        # Box para organizar texto e botões no rodapé
        footer_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=5)
        
        lbl_info = Gtk.Label()
        lbl_info.set_markup("<span size='small' color='#555555'>v1.0 ® <b>Dáviny Letícia Vidal</b></span>")
        footer_box.pack_start(lbl_info, False, False, 5)

        # Botão Sobre
        btn_about = Gtk.Button(label="Sobre")
        btn_about.set_relief(Gtk.ReliefStyle.NONE) # Estilo plano/limpo
        btn_about.connect("clicked", self.mostrar_sobre)
        footer_box.pack_end(btn_about, False, False, 2)

        self.main_layout.pack_start(footer_box, False, False, 0)

    def mostrar_sobre(self, btn):
        about = Gtk.AboutDialog()
        about.set_transient_for(self)
        about.set_program_name("Sistema de Avaliação GTK")
        about.set_version("1.0")
        about.set_copyright("Copyright © 2026 Dáviny Letícia Vidal")
        about.set_comments("Projeto desenvolvido para aulas que lecionam na ETEC.")
        about.set_website("https://vidal.press")
        about.set_website_label("vidal.press")
        about.set_authors(["Dáviny Letícia Vidal <hello@vidal.press>"])
        
        # Link do GitHub
        about.set_documenters(["https://github.com/davinyleticia/avalia-o-gtk-etec: https://github.com/davinyleticia/avalia-o-gtk-etec"])
        
        # Licença GNU
        about.set_license_type(Gtk.License.GPL_3_0) # Define automaticamente a licença GNU v3
        
        about.run()
        about.destroy()

    # --- MÉTODOS DE TELA (IGUAIS AO ANTERIOR) ---
    def tela_cadastro(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15, margin=30)
        self.ent_nome = Gtk.Entry(placeholder_text="Nome Completo")
        self.ent_rm = Gtk.Entry(placeholder_text="RM")
        self.cb_disciplina = Gtk.ComboBoxText()
        for d in ["Desenv. de Sistemas - A", "Desenv. de Sistemas - B", "POO"]: self.cb_disciplina.append_text(d)
        self.cb_disciplina.set_active(0)
        btn = Gtk.Button(label="Começar Avaliação")
        btn.connect("clicked", lambda x: self.stack.set_visible_child_name("questoes"))
        for w in [self.ent_nome, self.ent_rm, self.cb_disciplina, btn]: vbox.pack_start(w, False, False, 0)
        self.stack.add_named(vbox, "cadastro")

    def tela_questoes_paginada(self):
        self.vbox_questoes = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20, margin=40)
        self.lbl_pergunta = Gtk.Label(use_markup=True, xalign=0)
        self.box_opcoes = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        bbox = Gtk.ButtonBox(orientation=Gtk.Orientation.HORIZONTAL)
        self.btn_anterior = Gtk.Button(label="Anterior")
        self.btn_proxima = Gtk.Button(label="Próxima")
        self.btn_anterior.connect("clicked", self.mudar_pergunta, -1)
        self.btn_proxima.connect("clicked", self.mudar_pergunta, 1)
        bbox.add(self.btn_anterior); bbox.add(self.btn_proxima)
        self.barra_progresso = Gtk.ProgressBar()
        for w in [self.lbl_pergunta, self.box_opcoes, bbox, self.barra_progresso]: self.vbox_questoes.add(w)
        self.atualizar_interface_pergunta()
        self.stack.add_named(self.vbox_questoes, "questoes")

    def mudar_pergunta(self, btn, direcao):
        self.indice_atual += direcao
        if self.indice_atual >= len(self.questoes): self.gerar_token_final(None)
        else: self.atualizar_interface_pergunta()

    def atualizar_interface_pergunta(self):
        q = self.questoes[self.indice_atual]
        self.lbl_pergunta.set_markup(f"<b>Questão {self.indice_atual + 1} de {len(self.questoes)}</b>\n\n{q['p']}")
        for child in self.box_opcoes.get_children(): child.destroy()
        grupo = None
        for opcao in q['opts']:
            rb = Gtk.RadioButton.new_with_label_from_widget(grupo, opcao)
            if grupo is None: grupo = rb
            if self.respostas_selecionadas[self.indice_atual] == opcao: rb.set_active(True)
            rb.connect("toggled", self.ao_selecionar, self.indice_atual, opcao)
            self.box_opcoes.pack_start(rb, False, False, 0)
        self.btn_anterior.set_sensitive(self.indice_atual > 0)
        self.btn_proxima.set_label("Finalizar" if self.indice_atual == len(self.questoes)-1 else "Próxima")
        self.barra_progresso.set_fraction((self.indice_atual + 1) / len(self.questoes))
        self.show_all()

    def ao_selecionar(self, rb, indice, opcao):
        if rb.get_active(): self.respostas_selecionadas[indice] = opcao

    def tela_finalizacao(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15, margin=30)
        self.txt_codigo = Gtk.TextView(editable=False, wrap_mode=Gtk.WrapMode.WORD_CHAR)
        sw = Gtk.ScrolledWindow(); sw.add(self.txt_codigo)
        btn_sair = Gtk.Button(label="Fechar Sistema"); btn_sair.connect("clicked", Gtk.main_quit)
        vbox.pack_start(Gtk.Label(label="<b>Código de Entrega:</b>", use_markup=True), False, False, 0)
        vbox.pack_start(sw, True, True, 0); vbox.pack_start(btn_sair, False, False, 0)
        self.stack.add_named(vbox, "finalizacao")

    def gerar_token_final(self, btn):
        dados = {"nome": self.ent_nome.get_text(), "rm": self.ent_rm.get_text(), 
                 "disciplina": self.cb_disciplina.get_active_text(),
                 "data": datetime.now().strftime("%d/%m/%Y %H:%M"), "respostas": self.respostas_selecionadas}
        token = cipher_suite.encrypt(json.dumps(dados).encode())
        self.txt_codigo.get_buffer().set_text(token.decode())
        self.stack.set_visible_child_name("finalizacao")

if __name__ == "__main__":
    app = AppAluno()
    Gtk.main()