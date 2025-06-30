from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget
from PyQt6.QtCore import Qt
import sqlite3

class TelaPesquisa(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pesquisa")
        self.setFixedSize(400, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Digite um termo para buscar...")
        layout.addWidget(self.search_input)

        self.search_button = QPushButton("Buscar")
        self.search_button.clicked.connect(self.buscar)
        layout.addWidget(self.search_button)

        self.result_list = QListWidget()
        layout.addWidget(self.result_list)

        self.setLayout(layout)

    def buscar(self):
        termo = self.search_input.text()
        conn = sqlite3.connect("db/usuarios.db")
        cursor = conn.cursor()
        self.result_list.clear()
        try:
            cursor.execute("SELECT titulo, data FROM testes WHERE titulo LIKE ?", (f"%{termo}%",))
            resultados = cursor.fetchall()
            for r in resultados:
                self.result_list.addItem(f"{r[0]} - {r[1]}")
        except Exception as e:
            self.result_list.addItem(f"Erro na busca: {str(e)}")
        finally:
            conn.close()