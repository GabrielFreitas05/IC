from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame,
    QSizePolicy, QSpacerItem, QMessageBox
)
from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtCore import Qt
from telas.tela_testes import tela_testes
from telas.tela_gerenciar_processos import TelaGerenciarProcessos
from telas.tela_buscador_artigos import TelaBuscadorArtigos
from db.db import buscar_nome_usuario
from ui.components import HeaderBar, Card, set_variant
import os


class HoverButton(QPushButton):
    """
    Botão da sidebar (navegação). Mantém o comportamento original.
    Visual ajustado para harmonizar com o tema (transparente no fundo escuro).
    """
    def __init__(self, text, icon_path=None, function=None, enabled=True):
        super().__init__(text)
        self.function = function
        self.enabled = enabled
        if icon_path and os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QPixmap(icon_path).rect().size())
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #FFCD00;
                font-size: 15px;
                text-align: left;
                padding: 10px 14px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: rgba(255, 205, 0, 0.10);
            }
        """)

    def mousePressEvent(self, event):
        if self.enabled and self.function:
            self.function()


class SideBar(QWidget):
    """
    Sidebar de navegação. Fluxo de telas mantido.
    """
    def __init__(self, usuario_window, usuario_id):
        super().__init__()
        self.usuario_window = usuario_window
        self.usuario_id = usuario_id

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        logo = QLabel("SGCI")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("font-size: 20px; color: white; font-weight: bold;")
        layout.addWidget(logo)

        def abrir_tela_gerenciar_processos(uid):
            tela = TelaGerenciarProcessos(uid)
            tela.show()
            return tela

        def abrir_tela_buscador_artigos(uid):
            tela = TelaBuscadorArtigos(uid)
            tela.show()
            return tela

        def create_button(text, icon=None, function=None):
            def action():
                self.usuario_window.hide()
                nova_tela = function(self.usuario_id)
                self.usuario_window.nova_tela = nova_tela
            return HoverButton(text, icon_path=icon, function=action)

        layout.addWidget(create_button("POP", "assets/icon_pop.png", tela_testes))
        layout.addWidget(create_button("Processos", "assets/icon_pta.png", abrir_tela_gerenciar_processos))
        layout.addWidget(create_button("Buscar Artigos", "assets/icon_pta.png", abrir_tela_buscador_artigos))
        layout.addStretch()

        def confirmar_saida():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Question)
            msg.setWindowTitle("Confirmação")
            msg.setText("Deseja realmente sair?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            resultado = msg.exec()
            if resultado == QMessageBox.StandardButton.Yes:
                self.usuario_window.close()

        btn_sair = QPushButton("Sair")
        set_variant(btn_sair, "danger")
        btn_sair.clicked.connect(confirmar_saida)
        layout.addWidget(btn_sair)

        # Versão
        versao = QLabel("v1.0.0  © Capsnano")
        versao.setAlignment(Qt.AlignmentFlag.AlignCenter)
        versao.setStyleSheet("font-size: 10px; color: gray;")
        layout.addWidget(versao)

        self.setLayout(layout)
        self.setFixedWidth(220)
        self.setStyleSheet("""
            background-color: #12151c;  /* combina com tema dark */
            border-right: 1px solid #1e293b;
        """)


def gerar_iniciais(nome_usuario):
    partes = nome_usuario.split()
    iniciais = ''.join([parte[0].upper() for parte in partes if parte])
    return iniciais


def gerar_id_formatado(iniciais, usuario_id):
    numero = f"{usuario_id:03d}"
    return f"{iniciais}-{numero}"


def tela_usuario(usuario_id):
    """
    Tela inicial do usuário — agora com HeaderBar + Card (apenas design).
    """
    usuario_window = QWidget()
    usuario_window.setWindowTitle("Tela Inicial")
    usuario_window.setFixedSize(1000, 600)

    main_layout = QHBoxLayout()
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.setSpacing(0)


    sidebar = SideBar(usuario_window, usuario_id)
    main_layout.addWidget(sidebar)

    content_layout = QVBoxLayout()
    content_layout.setSpacing(16)
    content_layout.setContentsMargins(24, 24, 24, 24)

    header = HeaderBar("Tela Inicial", [])
    content_layout.addWidget(header)

    card = Card()
    card.lay.setSpacing(12)

    nome_usuario = buscar_nome_usuario(usuario_id)
    titulo = QLabel(f"Bem-vindo, {nome_usuario}")
    titulo.setObjectName("title")
    titulo.setAlignment(Qt.AlignmentFlag.AlignLeft)

    subtitulo = QLabel("Sistema de Gestão de Conhecimento e Inovação")
    subtitulo.setStyleSheet("color: #a7b2c3;")
    subtitulo.setAlignment(Qt.AlignmentFlag.AlignLeft)

    card.lay.addWidget(titulo)
    card.lay.addWidget(subtitulo)

    if os.path.exists("assets/logo.png"):
        logo = QLabel()
        pixmap = QPixmap("assets/logo.png").scaled(110, 110, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        card.lay.addWidget(logo)

    linha = QFrame()
    linha.setFrameShape(QFrame.Shape.HLine)
    linha.setFrameShadow(QFrame.Shadow.Plain)
    linha.setStyleSheet("color: #1e293b;")
    card.lay.addWidget(linha)
    card.lay.addStretch()
    content_layout.addWidget(card)
    main_layout.addLayout(content_layout)
    usuario_window.setLayout(main_layout)
    usuario_window.show()
    return usuario_window
