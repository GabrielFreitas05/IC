from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

def tela_pesquisa():
    app = QApplication([])

    pesquisa_window = QWidget()
    pesquisa_window.setWindowTitle("Pesquisa")
    pesquisa_window.setFixedSize(400, 400)

    bg_color = QColor("#1B3A5E")
    fg_color = QColor("#FFCD00")

    pesquisa_window.setStyleSheet(f"""
        background-color: {bg_color.name()};
        font-family: Arial, sans-serif;
    """)

    layout = QVBoxLayout()

    title_label = QLabel("Pesquisar Dados")
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {fg_color.name()};")
    layout.addWidget(title_label)

    search_input = QLineEdit()
    search_input.setPlaceholderText("Digite sua pesquisa")
    search_input.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #ccc;")
    layout.addWidget(search_input)

    search_button = QPushButton("Pesquisar")
    search_button.setStyleSheet(f"""
        background-color: {fg_color.name()};
        color: #1B3A5E;
        font-size: 16px;
        border-radius: 5px;
        padding: 10px;
    """)
    layout.addWidget(search_button)

    results_list = QListWidget()
    results_list.setStyleSheet("border-radius: 5px; border: 1px solid #ccc;")
    layout.addWidget(results_list)

    pesquisa_window.setLayout(layout)
    pesquisa_window.show()
    app.exec()