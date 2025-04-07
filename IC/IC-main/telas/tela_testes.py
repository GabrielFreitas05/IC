from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QPushButton, QLabel, 
    QSpacerItem, QSizePolicy, QDateEdit, QScrollArea, QTextEdit, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from db import db  # Alteração aqui para usar o import correto

bg_color = "#1B3A5E"
fg_color = "#FFCD00"

class HoverButton(QPushButton):
    def __init__(self, text, function):
        super().__init__(text)
        self.function = function

    def enterEvent(self, event):
        self.setStyleSheet(f"""
            background-color: {fg_color};
            color: #1B3A5E;
            font-size: 16px;
            font-weight: bold;
            border-radius: 25px;
            padding: 12px 25px;
            border: 2px solid {fg_color};
        """)

    def leaveEvent(self, event):
        self.setStyleSheet(f"""
            background-color: #1B3A5E;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 25px;
            padding: 12px 25px;
            border: 2px solid #1B3A5E;
        """)

    def mousePressEvent(self, event):
        self.function()

def exibir_erro(titulo, mensagem):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(titulo)
    msg.setText(mensagem)
    msg.exec()

def exibir_sucesso(titulo, mensagem):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setWindowTitle(titulo)
    msg.setText(mensagem)
    msg.exec()

def tela_testes(usuario_id):
    testes_window = QWidget()
    testes_window.setWindowTitle("POP's")
    testes_window.setFixedSize(850, 650)
    testes_window.setStyleSheet("background-color: #e0e0e0;")

    layout = QVBoxLayout()
    title_label = QLabel("Cadastro de POP (Procedimento Operacional Padrão)")
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_label.setFont(QFont("Helvetica", 18, QFont.Weight.Bold))
    title_label.setStyleSheet(f"color: {fg_color};")
    layout.addWidget(title_label)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setStyleSheet("background-color: #ffffff;")
    container_widget = QWidget()
    form_layout = QFormLayout()

    campos = [
        "Título do Procedimento", "Código do Documento", "Versão", "Data de Emissão",
        "Responsável", "Objetivo", "Aplicação e Escopo", "Responsabilidades",
        "Materiais e Equipamentos", "Procedimento Operacional", "Preparação",
        "Operação", "Finalização", "Seguranças e Riscos", "Anexos", "Histórico de Revisões"
    ]
    
    entradas = {}
    for campo in campos:
        label = QLabel(f"{campo}:")
        label.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
        label.setStyleSheet(f"color: {fg_color};")

        if campo == "Data de Emissão":
            entradas[campo] = QDateEdit()
            entradas[campo].setDisplayFormat("dd/MM/yyyy")
            entradas[campo].setDate(QDate.currentDate())
        else:
            entradas[campo] = QTextEdit()
        
        entradas[campo].setFont(QFont("Helvetica", 12))
        entradas[campo].setStyleSheet("background-color: #ffffff; border: 2px solid #1B3A5E; padding: 5px;")
        form_layout.addRow(label, entradas[campo])

    def selecionar_anexo():
        arquivo, _ = QFileDialog.getOpenFileName(testes_window, "Selecionar arquivo", "", "Imagens (*.jpg *.jpeg *.png *.gif);;Todos os Arquivos (*)")
        if arquivo:
            entradas["Anexos"].setText(arquivo)

    form_layout.addRow(HoverButton("Selecionar Anexo", selecionar_anexo))
    container_widget.setLayout(form_layout)
    scroll_area.setWidget(container_widget)
    layout.addWidget(scroll_area)

    def salvar():
        valores = {
            "titulo_procedimento": entradas["Título do Procedimento"].toPlainText().strip(),
            "codigo_documento": entradas["Código do Documento"].toPlainText().strip(),
            "versao": entradas["Versão"].toPlainText().strip(),
            "data_emissao": entradas["Data de Emissão"].date().toString("dd/MM/yyyy"),
            "responsavel": entradas["Responsável"].toPlainText().strip(),
            "objetivo": entradas["Objetivo"].toPlainText().strip(),
            "aplicacao_escopo": entradas["Aplicação e Escopo"].toPlainText().strip(),
            "responsabilidades": entradas["Responsabilidades"].toPlainText().strip(),
            "materiais_equipamentos": entradas["Materiais e Equipamentos"].toPlainText().strip(),
            "procedimento_operacional": entradas["Procedimento Operacional"].toPlainText().strip(),
            "preparacao": entradas["Preparação"].toPlainText().strip(),
            "operacao": entradas["Operação"].toPlainText().strip(),
            "finalizacao": entradas["Finalização"].toPlainText().strip(),
            "segurancas_riscos": entradas["Seguranças e Riscos"].toPlainText().strip(),
            "anexos": entradas["Anexos"].toPlainText().strip(),
            "historico_revisoes": entradas["Histórico de Revisões"].toPlainText().strip(),
        }

        if any(not v for v in valores.values()):
            exibir_erro("Erro", "Todos os campos devem ser preenchidos.")
            return

        db.salvar_teste(usuario_id, **valores)
        exibir_sucesso("Sucesso", "Procedimento salvo com sucesso.")

    layout.addWidget(HoverButton("Salvar POP", salvar))
    layout.addWidget(HoverButton("Voltar", lambda: (testes_window.close(), __import__('telas.tela_usuario').tela_usuario.tela_usuario(usuario_id))))

    testes_window.setLayout(layout)
    testes_window.show()
