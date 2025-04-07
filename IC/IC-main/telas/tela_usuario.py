from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from telas.tela_testes import tela_testes
from telas.tela_pesquisa import tela_pesquisa
from telas.tela_historico import tela_historico
from telas.tela_pta import tela_pta

class HoverButton(QPushButton):
    def __init__(self, text, function):
        super().__init__(text)
        self.function = function
        self.setStyleSheet("""
            background-color: #1B3A5E; 
            color: #FFFFFF; 
            font-size: 16px; 
            font-weight: bold; 
            border-radius: 25px; 
            padding: 12px 25px; 
            border: 2px solid #1B3A5E;
        """)

    def enterEvent(self, event):
        self.setStyleSheet("""
            background-color: #FFCD00; 
            color: #1B3A5E; 
            font-size: 16px; 
            font-weight: bold; 
            border-radius: 25px; 
            padding: 12px 25px; 
            border: 2px solid #FFCD00;
        """)

    def leaveEvent(self, event):
        self.setStyleSheet("""
            background-color: #1B3A5E; 
            color: #FFFFFF; 
            font-size: 16px; 
            font-weight: bold; 
            border-radius: 25px; 
            padding: 12px 25px; 
            border: 2px solid #1B3A5E;
        """)

    def mousePressEvent(self, event):
        self.function()

def tela_usuario(usuario_id):
    usuario_window = QWidget()
    usuario_window.setWindowTitle("Tela Inicial")
    usuario_window.setFixedSize(650, 500)

    bg_color = QColor("#1B3A5E")
    fg_color = QColor("#FFCD00")

    usuario_window.setStyleSheet(f"""
        background-color: {bg_color.name()};
        border-radius: 10px;
        font-family: Arial, sans-serif;
    """)

    layout = QVBoxLayout()

    title_label = QLabel("Bem-vindo ao Sistema")
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {fg_color.name()};")
    layout.addWidget(title_label)

    spacer = QSpacerItem(20, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    layout.addItem(spacer)

    def create_button(text, function):
        button = HoverButton(text, lambda: [usuario_window.close(),])
        button.setFixedHeight(50)
        layout.addWidget(button)

    create_button("Procedimento Operacional Padrão (POP)", tela_testes)
    create_button("PTA", tela_pta)
    create_button("Pesquisar Dados", tela_pesquisa)
    create_button("Meu Histórico de Dados", tela_historico)

    layout.addItem(spacer)

    usuario_window.setLayout(layout)
    usuario_window.show()
