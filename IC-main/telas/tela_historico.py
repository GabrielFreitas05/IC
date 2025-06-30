from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

def tela_historico():
    app = QApplication([])

    historico_window = QWidget()
    historico_window.setWindowTitle("Histórico")
    historico_window.setFixedSize(400, 400)

    # Cores do tema
    bg_color = QColor("#1B3A5E")
    fg_color = QColor("#FFCD00")

    historico_window.setStyleSheet(f"""
        background-color: {bg_color.name()};
        font-family: Arial, sans-serif;
    """)

    layout = QVBoxLayout()

    title_label = QLabel("Meu Histórico")
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {fg_color.name()};")
    layout.addWidget(title_label)

    results_list = QListWidget()
    results_list.setStyleSheet("border-radius: 5px; border: 1px solid #ccc;")
    layout.addWidget(results_list)

    back_button = QPushButton("Voltar")
    back_button.setStyleSheet(f"""
        background-color: {fg_color.name()};
        color: #1B3A5E;
        font-size: 16px;
        border-radius: 5px;
        padding: 10px;
    """)
    layout.addWidget(back_button)

    historico_window.setLayout(layout)
    historico_window.show()
    app.exec()