
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpacerItem,
    QSizePolicy, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor, QIcon
from telas.tela_testes import tela_testes
from telas.tela_pesquisa import TelaPesquisa
from telas.tela_historico import tela_historico
from telas.tela_gerenciar_processos import TelaGerenciarProcessos
from db.db import buscar_nome_usuario, buscar_id_usuario
import os

class HoverButton(QPushButton):
    def __init__(self, text, icon_path=None, function=None, enabled=True):
        super().__init__(text)
        self.function = function
        self.enabled = enabled
        if icon_path and os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QPixmap(icon_path).rect().size())
        self.update_style()

    def update_style(self):
        if self.enabled:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #FFCD00;
                    color: #1B3A5E;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 15px;
                    padding: 15px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #e5b800;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #cccccc;
                    color: #666666;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 15px;
                    padding: 15px;
                }
            """)
            self.setEnabled(False)

    def mousePressEvent(self, event):
        if self.enabled and self.function:
            self.function()

def tela_usuario(usuario_id):
    usuario_window = QWidget()
    usuario_window.setWindowTitle("Tela Inicial")
    usuario_window.setFixedSize(700, 550)

    bg_color = "#1B3A5E"
    fg_color = "#FFCD00"

    usuario_window.setStyleSheet(f"background-color: {bg_color};")

    layout = QVBoxLayout()
    layout.setSpacing(20)

    nome_usuario = buscar_nome_usuario(usuario_id)
    iniciais = gerar_iniciais(nome_usuario)
    usuario_id_formatado = gerar_id_formatado(iniciais, usuario_id)

    title = QLabel(f"Bem-vindo, {nome_usuario}")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setStyleSheet("font-size: 26px; color: white; font-weight: bold;")
    layout.addWidget(title)

    subtitle = QLabel("Sistema de Gestão de Conhecimento e Inovação")
    subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
    subtitle.setStyleSheet(f"font-size: 16px; color: {fg_color};")
    layout.addWidget(subtitle)

    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        logo = QLabel()
        pixmap = QPixmap(logo_path).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)

    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFrameShadow(QFrame.Shadow.Sunken)
    line.setStyleSheet("color: white;")
    layout.addWidget(line)

    button_layout = QHBoxLayout()
    button_layout.setSpacing(20)

    def abrir_tela_gerenciar_processos(uid):
        tela = TelaGerenciarProcessos(uid)
        tela.show()
        return tela

    def create_button(text, icon=None, function=None, enabled=True):
        def action():
            usuario_window.hide()
            nova_tela = function(usuario_id)
            usuario_window.nova_tela = nova_tela
        return HoverButton(text, icon_path=icon, function=action, enabled=enabled)

    button_layout.addWidget(create_button("POP", "assets/icon_pop.png", tela_testes, True))
    button_layout.addWidget(create_button("Processos", "assets/icon_pta.png", abrir_tela_gerenciar_processos, True))

    layout.addLayout(button_layout)

    id_label = QLabel(f"ID: {usuario_id_formatado}")
    id_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
    id_label.setStyleSheet("font-size: 12px; color: white; margin-right: 10px; margin-bottom: 10px;")
    layout.addWidget(id_label)

    usuario_window.setLayout(layout)
    usuario_window.show()
    return usuario_window

def gerar_iniciais(nome_usuario):
    partes = nome_usuario.split()
    iniciais = ''.join([parte[0].upper() for parte in partes if parte])
    return iniciais

def gerar_id_formatado(iniciais, usuario_id):
    numero = f"{usuario_id:03d}"
    return f"{iniciais}-{numero}"

