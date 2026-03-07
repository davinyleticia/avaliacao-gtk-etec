import gi
import pandas as pd
import json
from cryptography.fernet import Fernet

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

CHAVE = b'7P9Xj4kL_8z1nM5vR2uT6aB3cE0gH7iJ9kL2mN5oP8Q='
cipher_suite = Fernet(CHAVE)

# Gabarito oficial para as 10 questões
GABARITO = [
    "git init", "git commit", "Herança", "Encapsulamento", "Classe", 
    "cd", "ls", "Ver processos e CPU", "cd ..", "pwd"
]

class AppProfessor(Gtk.Window):
    def __init__(self):
        super().__init__(title="Painel de Correção - Vidal Press")
        self.set_default_size(550, 450)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        self.main_layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.main_layout)
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15, margin=30)
        self.main_layout.pack_start(vbox, True, True, 0)
        
        lbl = Gtk.Label(label="<span size='large'><b>Processador de Notas</b></span>", use_markup=True)
        btn_abrir = Gtk.Button(label="Carregar CSV de Entregas")
        btn_abrir.connect("clicked", self.on_file_clicked)
        
        sw = Gtk.ScrolledWindow()
        self.txt_log = Gtk.TextView(editable=False)
        sw.add(self.txt_log)
        
        vbox.pack_start(lbl, False, False, 0)
        vbox.pack_start(btn_abrir, False, False, 10)
        vbox.pack_start(Gtk.Label(label="Status do Processamento:", xalign=0), False, False, 0)
        vbox.pack_start(sw, True, True, 0)
        
        self.criar_footer()
        self.show_all()
        self.connect("destroy", Gtk.main_quit)

    def criar_footer(self):
        separador = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.main_layout.pack_start(separador, False, False, 5)

        footer_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=5)
        
        lbl_footer = Gtk.Label()
        lbl_footer.set_markup("<span size='small' color='#555555'>v1.0 ® <b>Dáviny L. Vidal</b></span>")
        footer_box.pack_start(lbl_footer, False, False, 10)

        # Botão Sobre que abre o diálogo com Licença GNU
        btn_about = Gtk.Button(label="Sobre")
        btn_about.set_relief(Gtk.ReliefStyle.NONE)
        btn_about.connect("clicked", self.mostrar_sobre)
        footer_box.pack_end(btn_about, False, False, 5)

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

    def log(self, msg):
        buf = self.txt_log.get_buffer()
        buf.insert(buf.get_end_iter(), msg + "\n")

    def calcular_mencao(self, acertos):
        # Lógica para 10 questões
        if acertos >= 9: return "MB"
        if acertos >= 7: return "B"
        if acertos >= 5: return "R"
        return "I"

    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(title="Selecione o CSV", parent=self, action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        if dialog.run() == Gtk.ResponseType.OK:
            self.processar(dialog.get_filename())
        dialog.destroy()

    def processar(self, caminho):
        try:
            df = pd.read_csv(caminho)
            resultados = []
            for i, row in df.iterrows():
                try:
                    token = row['codigo'].strip()
                    dados = json.loads(cipher_suite.decrypt(token.encode()))
                    
                    # Correção baseada no GABARITO global
                    acertos = sum(1 for idx, r in enumerate(dados['respostas']) if r == GABARITO[idx])
                    
                    resultados.append({
                        "Nome": dados['nome'],
                        "RM": dados['rm'],
                        "Disciplina": dados['disciplina'],
                        "Acertos": acertos,
                        "Mencao": self.calcular_mencao(acertos),
                        "Data_Entrega": dados.get("data", "N/A")
                    })
                    self.log(f"Processado: {dados['nome']} - {self.calcular_mencao(acertos)}")
                except: 
                    self.log(f"Erro na linha {i+1}: Token inválido ou corrompido.")
            
            pd.DataFrame(resultados).to_csv("notas_finais_completas.csv", index=False, encoding='utf-8-sig')
            self.log("\n>>> Sucesso! Arquivo 'notas_finais_completas.csv' gerado.")
        except Exception as e: 
            self.log(f"Erro crítico ao ler o arquivo: {e}")

if __name__ == "__main__":
    app = AppProfessor()
    Gtk.main()