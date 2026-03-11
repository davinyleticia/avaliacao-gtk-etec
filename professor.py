import gi
import pandas as pd
import json
from datetime import datetime
from cryptography.fernet import Fernet

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# MESMA CHAVE USADA NO APP DO ALUNO
CHAVE = b'7P9Xj4kL_8z1nM5vR2uT6aB3cE0gH7iJ9kL2mN5oP8Q='
cipher_suite = Fernet(CHAVE)

# Gabarito mapeado por disciplina
GABARITOS_MULTIDISCIPLINAR = {
    "Desenvolvimento de Sistemas II": [
        "git init", "git commit", "git push", "Adiciona mensagem", "git status",
        "git pull", "git add .", "git log", "A branch principal", "git branch nome"
    ],
    "POO (Prog. Orientada a Objetos)": [
        "Um molde/plano", "Herança", "Encapsulamento", "Uma instância de classe", "Ações/Comportamentos",
        "Características/Dados", "Múltiplas formas", "public", "Inicializar o objeto", "Classe que não vira objeto"
    ],
    "PW I (HTML Básico)": [
        "<title>", "<a>", "<ul>", "<img src='...'>", "<body>",
        "<h1>", "href", "<br>", "Metadados/Configurações", "<table>"
    ],
    "PW III (Next.js & DNS)": [
        "Converte nomes em IPs", "Peças de UI reutilizáveis", "npx create-next-app", "/app", "Server Side Rendering",
        "53", "import", "layout.js", "Vercel", "React"
    ],
    "PAM (Mobile - Expo)": [
        "Plataforma para React Native", "<Text>", "<View>", "npx expo start", "Ambos",
        "JavaScript/TypeScript", "Atualiza o app ao salvar", "StyleSheet", "npm install", "Expo Go"
    ],
    "Sistemas Operacionais (Linux)": [
        "ls", "pwd", "cd", "Monitorar processos/CPU", "mkdir",
        "rm", "cat", "Limpa a tela", "sudo", "exit"
    ]
}

class AppProfessor(Gtk.Window):
    def __init__(self):
        super().__init__(title="Painel de Correção v1.1 - Vidal Press")
        self.set_default_size(600, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        self.main_layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.main_layout)
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15, margin=30)
        self.main_layout.pack_start(vbox, True, True, 0)
        
        lbl = Gtk.Label(label="<span size='large'><b>Processador de Notas Multidisciplinar</b></span>", use_markup=True)
        
        btn_abrir = Gtk.Button(label="Selecionar CSV de Respostas")
        btn_abrir.get_style_context().add_class("suggested-action")
        btn_abrir.connect("clicked", self.on_file_clicked)
        
        sw = Gtk.ScrolledWindow()
        self.txt_log = Gtk.TextView(editable=False, cursor_visible=False)
        self.txt_log.set_left_margin(10)
        sw.add(self.txt_log)
        
        vbox.pack_start(lbl, False, False, 0)
        vbox.pack_start(btn_abrir, False, False, 10)
        vbox.pack_start(Gtk.Label(label="Logs de Processamento:", xalign=0), False, False, 0)
        vbox.pack_start(sw, True, True, 0)
        
        self.criar_footer() # Rodapé com botão Sobre
        self.show_all()
        self.connect("destroy", Gtk.main_quit)

    def criar_footer(self):
        self.main_layout.pack_start(Gtk.Separator(), False, False, 5)
        footer_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin=5)
        
        lbl_footer = Gtk.Label()
        lbl_footer.set_markup("<span size='small' color='#555555'>v1.1 ® <b>Dáviny L. Vidal</b></span>")
        footer_box.pack_start(lbl_footer, False, False, 10)

        # Botão Sobre reintegrado
        btn_about = Gtk.Button(label="Sobre")
        btn_about.set_relief(Gtk.ReliefStyle.NONE)
        btn_about.connect("clicked", self.mostrar_sobre)
        footer_box.pack_end(btn_about, False, False, 5)

        self.main_layout.pack_start(footer_box, False, False, 0)

    def mostrar_sobre(self, btn):
        about = Gtk.AboutDialog()
        about.set_transient_for(self)
        about.set_program_name("Painel de Correção - Vidal Press")
        about.set_version("1.1")
        about.set_copyright("Copyright © 2026 Dáviny Letícia Vidal")
        about.set_comments("Ferramenta de processamento de notas para as disciplinas da ETEC.")
        about.set_website("https://vidal.press")
        about.set_website_label("vidal.press")
        about.set_authors(["Dáviny Letícia Vidal <hello@vidal.press>"])
        
        # Licença GNU
        about.set_license_type(Gtk.License.GPL_3_0)
        
        about.run()
        about.destroy()

    def log(self, msg):
        buf = self.txt_log.get_buffer()
        buf.insert(buf.get_end_iter(), f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")

    def calcular_mencao(self, acertos):
        if acertos >= 9: return "MB"
        if acertos >= 7: return "B"
        if acertos >= 5: return "R"
        return "I"

    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(title="Selecione o CSV", parent=self, action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        
        filtro_csv = Gtk.FileFilter()
        filtro_csv.set_name("Arquivos CSV")
        filtro_csv.add_pattern("*.csv")
        dialog.add_filter(filtro_csv)

        if dialog.run() == Gtk.ResponseType.OK:
            self.processar(dialog.get_filename())
        dialog.destroy()

    def processar(self, caminho):
        try:
            df = pd.read_csv(caminho)
            if 'codigo' not in df.columns:
                self.log("ERRO: O CSV deve conter uma coluna chamada 'codigo'.")
                return

            resultados = []
            processados = 0

            for i, row in df.iterrows():
                try:
                    token = str(row['codigo']).strip()
                    json_puro = cipher_suite.decrypt(token.encode()).decode()
                    dados = json.loads(json_puro)
                    
                    disciplina = dados.get('disciplina', 'Desconhecida')
                    respostas_aluno = dados.get('respostas', [])
                    
                    gabarito_correto = GABARITOS_MULTIDISCIPLINAR.get(disciplina)
                    
                    if gabarito_correto:
                        acertos = sum(1 for idx, r in enumerate(respostas_aluno) if r == gabarito_correto[idx])
                        mencao = self.calcular_mencao(acertos)
                    else:
                        acertos = 0
                        mencao = "ERRO (Gabarito ñ encontrado)"

                    resultados.append({
                        "Nome": dados.get('nome'),
                        "RM": dados.get('rm'),
                        "Disciplina": disciplina,
                        "Acertos": acertos,
                        "Mencao": mencao,
                        "Data_Entrega": dados.get("data", "N/A")
                    })
                    self.log(f"OK: {dados.get('nome')} [{disciplina}] -> {mencao}")
                    processados += 1
                except Exception as e: 
                    self.log(f"Linha {i+1}: Erro ao decodificar (Token inválido).")

            if resultados:
                nome_saida = f"notas_finais_{datetime.now().strftime('%d%m_%H%M')}.csv"
                pd.DataFrame(resultados).to_csv(nome_saida, index=False, encoding='utf-8-sig')
                self.log(f"\n>>> CONCLUÍDO: {processados} notas salvas em '{nome_saida}'")
            
        except Exception as e: 
            self.log(f"ERRO CRÍTICO: {e}")

if __name__ == "__main__":
    app = AppProfessor()
    Gtk.main()