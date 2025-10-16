import sqlite3
import bcrypt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from db.db import criar_pedido_cadastro
from utils.emailer import send_email

class AguardandoDialog(QDialog):
    def __init__(self, email, parent=None):
        super().__init__(parent)
        self.email = email
        self.setWindowTitle("Aguardando aprovação")
        self.setFixedSize(420, 220)
        self.setStyleSheet("""
            QDialog { background-color: #1A2A47; color: white; font-family: 'Segoe UI', sans-serif; }
            QPushButton { background-color: #FFCD00; color: #1B3A5E; font-weight: bold; border: none; padding: 10px; border-radius: 6px; }
            QPushButton:hover { background-color: #e6b800; }
            QLabel { color: white; }
        """)
        layout = QVBoxLayout(self)
        lbl = QLabel(f"Seu cadastro {email} aguarda aprovação do administrador.")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)
        btn_login = QPushButton("Voltar ao login")
        btn_sair = QPushButton("Sair")
        layout.addWidget(btn_login)
        layout.addWidget(btn_sair)
        btn_login.clicked.connect(self.voltar_login)
        btn_sair.clicked.connect(self.close)

    def voltar_login(self):
        try:
            from telas.tela_login import tela_login
            self.close()
            tela_login()
        except Exception:
            self.close()

def tela_registro():
    registro_window = QWidget()
    registro_window.setWindowTitle("Registro")
    registro_window.setFixedSize(420, 520)
    registro_window.setStyleSheet("""
        QWidget { background-color: #1A2A47; font-family: 'Segoe UI', sans-serif; color: white; }
        QLineEdit, QComboBox { background-color: #1a1a1d; border: none; border-bottom: 2px solid #FFCD00; padding: 10px; color: white; }
        QPushButton { background-color: #FFCD00; color: #1B3A5E; font-weight: bold; border: none; padding: 12px; border-radius: 6px; }
        QPushButton:hover { background-color: #e6b800; }
    """)

    layout = QVBoxLayout()
    layout.setContentsMargins(40, 40, 40, 40)
    layout.setSpacing(20)

    title_label = QLabel("Criar nova conta")
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
    layout.addWidget(title_label)

    nome_input = QLineEdit()
    nome_input.setPlaceholderText("Nome completo")
    layout.addWidget(nome_input)

    email_input = QLineEdit()
    email_input.setPlaceholderText("E-mail")
    layout.addWidget(email_input)

    senha_input = QLineEdit()
    senha_input.setPlaceholderText("Senha")
    senha_input.setEchoMode(QLineEdit.EchoMode.Password)
    layout.addWidget(senha_input)

    role_combo = QComboBox()
    role_combo.addItems(["user", "tech", "admin"])
    layout.addWidget(role_combo)

    btn_registrar = QPushButton("Solicitar cadastro")
    layout.addWidget(btn_registrar)

    def enviar():
        nome = nome_input.text().strip()
        email = email_input.text().strip().lower()
        senha = senha_input.text()
        requested_role = role_combo.currentText()
        if not nome or not email or not senha:
            QMessageBox.warning(registro_window, "Erro", "Preencha todos os campos.")
            return
        try:
            senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
        except Exception:
            QMessageBox.critical(registro_window, "Erro", "Falha ao processar a senha.")
            return
        try:
            criar_pedido_cadastro(email, nome, senha_hash, "", requested_role)
        except sqlite3.IntegrityError:
            QMessageBox.critical(registro_window, "Erro", "E-mail já utilizado.")
            return
        except Exception:
            QMessageBox.critical(registro_window, "Erro", "Falha ao salvar o pedido de cadastro.")
            return
        subject = "Novo pedido de cadastro pendente"
        body = f"Nome: {nome}\nE-mail: {email}\nNível solicitado: {requested_role}\nAprovar no Painel do Administrador."
        admins = ["gmaeagendamentos@gmail.com"]
        erros = []
        for adm in admins:
            ok, err = send_email(adm, subject, body)
            if not ok:
                erros.append(err)
        if erros:
            QMessageBox.warning(registro_window, "Aviso", "Pedido salvo, mas o e-mail ao administrador falhou.")
        else:
            QMessageBox.information(registro_window, "Enviado", "Seu pedido foi enviado para aprovação do administrador.")
        try:
            registro_window.hide()
            registro_window._aguardo = AguardandoDialog(email, parent=registro_window)
            registro_window._aguardo.show()
        except Exception as e:
            QMessageBox.information(registro_window, "Informação", "Cadastro enviado. Retornando ao login.")
            try:
                from telas.tela_login import tela_login
                registro_window.hide()
                tela_login()
            except Exception:
                pass

    btn_registrar.clicked.connect(enviar)
    registro_window.setLayout(layout)
    registro_window.show()
    return registro_window
