import sqlite3
import bcrypt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from telas.tela_usuario import tela_usuario
from telas.tela_registro import tela_registro
from telas.tela_admin import TelaAdmin
from db.connection import get_connection

ADMIN_EMAIL = "admin@admin.com"
ADMIN_PASSWORD_HASH = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()

def tela_login():
    login_window = QWidget()
    login_window.setWindowTitle("Login")
    login_window.setFixedSize(420, 520)
    login_window.setStyleSheet("""
        QWidget {
            background-color: #0f172a;
            font-family: 'Segoe UI', sans-serif;
            color: white;
        }
    """)

    layout = QVBoxLayout()
    layout.setContentsMargins(40, 40, 40, 40)
    layout.setSpacing(20)

    logo = QLabel()
    logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
    logo.setPixmap(QPixmap("assets/logo.jpg").scaledToWidth(100))
    layout.addWidget(logo)

    title_label = QLabel("Entrar na sua conta")
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
    layout.addWidget(title_label)

    email_input = QLineEdit()
    email_input.setPlaceholderText("E-mail")
    email_input.setStyleSheet("""
        background-color: #1a1a1d;
        border: none;
        border-bottom: 2px solid #FFCD00;
        padding: 10px;
        color: white;
    """)
    layout.addWidget(email_input)

    password_input = QLineEdit()
    password_input.setPlaceholderText("Senha")
    password_input.setEchoMode(QLineEdit.EchoMode.Password)
    password_input.setStyleSheet("""
        background-color: #1a1a1d;
        border: none;
        border-bottom: 2px solid #FFCD00;
        padding: 10px;
        color: white;
    """)
    layout.addWidget(password_input)

    login_button = QPushButton("Entrar")
    login_button.setCursor(Qt.CursorShape.PointingHandCursor)
    login_button.setStyleSheet("""
        background-color: #FFCD00;
        color: #1B3A5E;
        font-weight: bold;
        border: none;
        padding: 12px;
        border-radius: 6px;
    """)
    layout.addWidget(login_button)

    register_row = QHBoxLayout()
    register_label = QLabel("Não tem uma conta?")
    register_label.setStyleSheet("color: #bbb;")
    register_button = QPushButton("Registrar-se")
    register_button.setCursor(Qt.CursorShape.PointingHandCursor)
    register_button.setStyleSheet("""
        background: none;
        color: #FFCD00;
        border: none;
        font-weight: bold;
        text-decoration: underline;
    """)
    register_row.addWidget(register_label)
    register_row.addWidget(register_button)
    layout.addLayout(register_row)

    def autenticar_usuario():
        email = email_input.text().strip()
        senha = password_input.text().strip()

        if not email or not senha:
            QMessageBox.warning(login_window, "Erro", "Preencha todos os campos.")
            return

        if email == ADMIN_EMAIL:
            if bcrypt.checkpw(senha.encode(), ADMIN_PASSWORD_HASH.encode()):
                QMessageBox.information(login_window, "Sucesso", "Login do Administrador realizado com sucesso!")
                admin = TelaAdmin()
                admin.exec()
                login_window.close()
                return
            else:
                QMessageBox.warning(login_window, "Erro", "Senha do administrador incorreta.")
                return

        conn = get_connection("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("SELECT rowid, senha, is_active FROM usuarios WHERE email = ?", (email,))
        resultado = cursor.fetchone()
        conn.close()

        if not resultado:
            QMessageBox.warning(login_window, "Erro", "Usuário não encontrado.")
            return

        usuario_id, senha_hash, is_active = resultado

        if is_active != 1:
            QMessageBox.warning(login_window, "Erro", "Usuário ainda não aprovado pelo administrador.")
            return

        if isinstance(senha_hash, str):
            senha_hash_bytes = senha_hash.encode()
        else:
            senha_hash_bytes = senha_hash

        if bcrypt.checkpw(senha.encode(), senha_hash_bytes):
            QMessageBox.information(login_window, "Sucesso", "Login realizado com sucesso!")
            login_window.close()
            tela_usuario(usuario_id)
        else:
            QMessageBox.warning(login_window, "Erro", "Senha incorreta.")

    def abrir_tela_registro():
        login_window.close()
        tela_registro()

    login_button.clicked.connect(autenticar_usuario)
    register_button.clicked.connect(abrir_tela_registro)

    login_window.setLayout(layout)
    login_window.show()
