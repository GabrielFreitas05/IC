from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QLineEdit, QLabel, QMessageBox, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from db.db import excluir_usuario, excluir_teste, listar_usuarios, listar_pta, listar_testes

class TelaAdmin(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Painel do Administrador")
        self.setFixedSize(800, 600)
        self.setStyleSheet("""
            QDialog {
                background-color: #1A2A47;
                color: white;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton {
                background-color: #FFCD00;
                color: #1A2A47;
                font-weight: bold;
                border: none;
                padding: 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #e6b800;
            }
            QLineEdit {
                background-color: #1a1a1d;
                border: none;
                border-bottom: 2px solid #FFCD00;
                padding: 10px;
                color: white;
            }
            QLabel {
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        title_label = QLabel("Painel Administrativo")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        btn_listar_usuarios = QPushButton("Listar Usuários")
        btn_listar_usuarios.clicked.connect(self.listar_usuarios)
        layout.addWidget(btn_listar_usuarios)

        btn_listar_ptas = QPushButton("Listar PTAs")
        btn_listar_ptas.clicked.connect(self.listar_ptas)
        layout.addWidget(btn_listar_ptas)

        btn_listar_testes = QPushButton("Listar Testes")
        btn_listar_testes.clicked.connect(self.listar_testes)
        layout.addWidget(btn_listar_testes)

        self.usuario_id_input = QLineEdit()
        self.usuario_id_input.setPlaceholderText("ID do Usuário ou Teste para excluir")
        layout.addWidget(self.usuario_id_input)

        btn_excluir_usuario = QPushButton("Excluir Usuário")
        btn_excluir_usuario.clicked.connect(self.excluir_usuario)
        layout.addWidget(btn_excluir_usuario)

        btn_excluir_teste = QPushButton("Excluir Teste")
        btn_excluir_teste.clicked.connect(self.excluir_teste)
        layout.addWidget(btn_excluir_teste)

        self.tabela = QTableWidget()
        layout.addWidget(self.tabela)

        self.setLayout(layout)

    def listar_usuarios(self):
        usuarios = listar_usuarios()
        if usuarios:
            self.mostrar_dados(usuarios, "Usuários", ["ID", "Email", "Nome", "Senha"])
        else:
            QMessageBox.information(self, "Aviso", "Nenhum usuário encontrado.")

    def listar_ptas(self):
        ptas = listar_pta()
        if ptas:
            self.mostrar_dados(ptas, "PTAs", ["ID", "Data", "Descrição"])
        else:
            QMessageBox.information(self, "Aviso", "Nenhum PTA encontrado.")

    def listar_testes(self):
        testes = listar_testes()
        if testes:
            self.mostrar_dados(testes, "Testes", ["ID", "Título", "Código", "Responsável"])
        else:
            QMessageBox.information(self, "Aviso", "Nenhum teste encontrado.")

    def mostrar_dados(self, dados, tipo, colunas):
        self.tabela.setColumnCount(len(colunas))
        self.tabela.setRowCount(len(dados))
        self.tabela.setHorizontalHeaderLabels(colunas)

        for row_idx, row in enumerate(dados):
            for col_idx, valor in enumerate(row):
                item = QTableWidgetItem(str(valor))
                self.tabela.setItem(row_idx, col_idx, item)
        
        self.tabela.resizeColumnsToContents()

    def excluir_usuario(self):
        usuario_id = self.usuario_id_input.text()
        if usuario_id:
            try:
                excluir_usuario(usuario_id)
                QMessageBox.information(self, "Sucesso", f"Usuário {usuario_id} excluído com sucesso.")
                self.listar_usuarios()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao excluir usuário: {e}")
        else:
            QMessageBox.warning(self, "Aviso", "Por favor, insira um ID de usuário.")

    def excluir_teste(self):
        teste_id = self.usuario_id_input.text()
        if teste_id:
            try:
                excluir_teste(teste_id)
                QMessageBox.information(self, "Sucesso", f"Teste {teste_id} excluído com sucesso.")
                self.listar_testes()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao excluir teste: {e}")
        else:
            QMessageBox.warning(self, "Aviso", "Por favor, insira um ID de teste.")
