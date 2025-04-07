import sqlite3
import bcrypt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from telas.tela_usuario import tela_usuario
from telas.tela_registro import tela_registro

def tela_login():
    login_window = QWidget()
    login_window.setWindowTitle("Login")
    login_window.setFixedSize(400, 400)

    bg_color = QColor("#1B3A5E")
    fg_color = QColor("#FFCD00")

    login_window.setStyleSheet(f"""
        background-color: {bg_color.name()};
        font-family: Arial, sans-serif;
    """)

    layout = QVBoxLayout()

    title_label = QLabel("Login")
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {fg_color.name()};")
    layout.addWidget(title_label)

    email_input = QLineEdit()
    email_input.setPlaceholderText("E-mail")
    email_input.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #ccc;")
    layout.addWidget(email_input)

    password_input = QLineEdit()
    password_input.setPlaceholderText("Senha")
    password_input.setEchoMode(QLineEdit.EchoMode.Password)
    password_input.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #ccc;")
    layout.addWidget(password_input)

    login_button = QPushButton("Entrar")
    login_button.setStyleSheet(f"""
        background-color: {fg_color.name()};
        color: #1B3A5E;
        font-size: 16px;
        border-radius: 5px;
        padding: 10px;
    """)
    layout.addWidget(login_button)

    register_button = QPushButton("Registrar-se")
    register_button.setStyleSheet(f"""
        background-color: {fg_color.name()};
        color: #1B3A5E;
        font-size: 16px;
        border-radius: 5px;
        padding: 10px;
    """)
    layout.addWidget(register_button)

    def autenticar_usuario():
        email = email_input.text()
        senha = password_input.text()

        if not email or not senha:
            QMessageBox.warning(login_window, "Erro", "Preencha todos os campos.")
            return

        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("SELECT rowid, senha FROM usuarios WHERE email = ?", (email,))
        resultado = cursor.fetchone()
        conn.close()

        if not resultado:
            QMessageBox.warning(login_window, "Erro", "Usuário não encontrado.")
            return

        usuario_id, senha_hash = resultado

        if bcrypt.checkpw(senha.encode(), senha_hash):
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
