from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QListView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl
import requests

class TelaBuscadorArtigos(QWidget):
    def __init__(self, usuario_id):
        super().__init__()
        self.usuario_id = usuario_id
        self.setWindowTitle("Buscador de Artigos Científicos")
        self.setStyleSheet("background-color: #1B1F27; color: white; font-size: 14px;")
        self.setMinimumSize(800, 600)

        layout = QVBoxLayout(self)

        titulo = QLabel("Buscador de Artigos Científicos")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFCD00")
        layout.addWidget(titulo)

        barra_busca = QHBoxLayout()
        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("Digite o tema do artigo (ex: grafeno, machine learning...)")
        self.botao_buscar = QPushButton("Buscar")
        self.botao_buscar.setStyleSheet("background-color: #FFCD00; color: black; font-weight: bold;")
        self.botao_buscar.clicked.connect(self.buscar_artigos)

        barra_busca.addWidget(self.campo_busca)
        barra_busca.addWidget(self.botao_buscar)
        layout.addLayout(barra_busca)

        self.resultados = QListWidget()
        self.resultados.setStyleSheet("QListWidget{ background-color: #10131A; border: none; }")
        layout.addWidget(self.resultados)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.btn_voltar = QPushButton("← Voltar")
        self.btn_voltar.clicked.connect(self._voltar_tela_usuario)
        main_layout.addWidget(self.btn_voltar, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(main_layout)

    def _voltar_tela_usuario(self):
        from telas.tela_usuario import tela_usuario
        self.close()
        self.tela_usuario = tela_usuario(self.usuario_id)
        self.tela_usuario.show()

    def buscar_artigos(self):
        termo = self.campo_busca.text().strip()
        if not termo:
            return
        url = "https://api.crossref.org/works"
        params = {
            "query": termo,
            "rows": 50,
            "select": "title,author,URL",
            "sort": "relevance"
        }
        try:
            resposta = requests.get(url, params=params, timeout=30)
            resposta.raise_for_status()
            artigos = resposta.json()["message"]["items"]
            self.resultados.clear()
            for art in artigos:
                titulo = art.get("title", ["Sem título"])[0]
                autores = ", ".join([a.get("family", "") for a in art.get("author", [])]) or "Autor desconhecido"
                url = art.get("URL", "#")

                container = QWidget()
                container_layout = QVBoxLayout()
                container_layout.setSpacing(5)

                label_titulo = QLabel(f"<b>{titulo}</b>")
                label_autores = QLabel(f"Autores: {autores}")
                label_titulo.setStyleSheet("color: #FFCD00; font-size: 16px;")
                label_autores.setStyleSheet("color: white;")

                btn_abrir = QPushButton("ABRIR ARTIGO")
                btn_abrir.setStyleSheet("background-color: #FFCD00; color: black; font-weight: bold; padding: 5px;")
                btn_abrir.clicked.connect(lambda _, link=url: QDesktopServices.openUrl(QUrl(link)))
                btn_abrir.setFixedWidth(120)

                container_layout.addWidget(label_titulo)
                container_layout.addWidget(label_autores)
                container_layout.addWidget(btn_abrir)
                container.setLayout(container_layout)

                item = QListWidgetItem()
                item.setSizeHint(container.sizeHint())
                self.resultados.addItem(item)
                self.resultados.setItemWidget(item, container)
        except Exception as e:
            self.resultados.clear()
            self.resultados.addItem(f"Erro ao buscar: {str(e)}")
