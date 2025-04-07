from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
import sqlite3

def tela_pta(usuario_id):
    pta_window = QWidget()
    pta_window.setWindowTitle("PTA")
    pta_window.setFixedSize(400, 400)

    bg_color = QColor("#1B3A5E")
    fg_color = QColor("#FFCD00")

    pta_window.setStyleSheet(f"""
        background-color: {bg_color.name()};
        font-family: Arial, sans-serif;
    """)

    layout = QVBoxLayout()

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM usuarios WHERE id = ?", (usuario_id,))
    resultado = cursor.fetchone()
    conn.close()

    nome_usuario = resultado[0] if resultado else "Usuário Desconhecido"

    title_label = QLabel(f"PTA - Usuário: {nome_usuario}")
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {fg_color.name()};")
    layout.addWidget(title_label)

    description_input = QLineEdit()
    description_input.setPlaceholderText("Descrição do PTA")
    description_input.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #ccc;")
    layout.addWidget(description_input)

    submit_button = QPushButton("Enviar PTA")
    submit_button.setStyleSheet(f"""
        background-color: {fg_color.name()};
        color: #1B3A5E;
        font-size: 16px;
        border-radius: 5px;
        padding: 10px;
    """)
    layout.addWidget(submit_button)

    pta_window.setLayout(layout)
    pta_window.show()
