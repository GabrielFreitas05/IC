import sqlite3
import bcrypt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

def tela_registro():
    registro_window = QWidget()
    registro_window.setWindowTitle("Registro")
    registro_window.setFixedSize(400, 450)

    bg_color = QColor("#1B3A5E")
    fg_color = QColor("#FFCD00")

    registro_window.setStyleSheet(f"""
        background-color: {bg_color.name()};
        font-family: Arial, sans-serif;
    """)

    layout = QVBoxLayout()

    title_label = QLabel("Registro")
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {fg_color.name()};")
    layout.addWidget(title_label)

    nome_input = QLineEdit()
    nome_input.setPlaceholderText("Nome completo")
    nome_input.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #ccc;")
    layout.addWidget(nome_input)

    email_input = QLineEdit()
    email_input.setPlaceholderText("E-mail")
    email_input.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #ccc;")
    layout.addWidget(email_input)

    password_input = QLineEdit()
    password_input.setPlaceholderText("Senha")
    password_input.setEchoMode(QLineEdit.EchoMode.Password)
    password_input.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #ccc;")
    layout.addWidget(password_input)

    register_button = QPushButton("Registrar")
    register_button.setStyleSheet(f"""
        background-color: {fg_color.name()};
        color: #1B3A5E;
        font-size: 16px;
        border-radius: 5px;
        padding: 10px;
    """)
    layout.addWidget(register_button)

    def registrar_usuario():
        nome = nome_input.text()
        email = email_input.text()
        senha = password_input.text()

        if not nome or not email or not senha:
            QMessageBox.warning(registro_window, "Erro", "Por favor, preencha todos os campos.")
            return
        if "@" not in email:
            QMessageBox.warning(registro_window, "Erro", "E-mail inválido. Deve conter '@'.")
            return
        if len(senha) < 6:
            QMessageBox.warning(registro_window, "Erro", "A senha deve ter pelo menos 6 caracteres.")
            return

        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, email TEXT UNIQUE, senha TEXT)")
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        if cursor.fetchone():
            QMessageBox.warning(registro_window, "Erro", "E-mail já cadastrado.")
            conn.close()
            return

        hashed = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, hashed))
        conn.commit()
        conn.close()
        QMessageBox.information(registro_window, "Sucesso", "Usuário registrado com sucesso!")
        registro_window.close()

        from telas.tela_login import tela_login 
        tela_login() 

    register_button.clicked.connect(registrar_usuario)

    registro_window.setLayout(layout)
    registro_window.show()
