import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QPushButton, QLabel,
    QDateEdit, QScrollArea, QTextEdit, QFileDialog, QMessageBox, QHBoxLayout, QListWidget, QListWidgetItem, QLineEdit, QInputDialog
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from db import db
from telas.preencher_pop import preencher_pop

bg_color = "#1B3A5E"
fg_color = "#FFCD00"
button_hover_color = "#FFB800"
input_hover_color = "#E8E8E8"
button_click_color = "#FF8000"

class HoverButton(QPushButton):
    def __init__(self, text, function):
        super().__init__(text)
        self.function = function
        self.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.setStyleSheet(f"""
            background-color: {bg_color};
            color: white;
            border-radius: 12px;
            padding: 10px 20px;
            border: 2px solid {bg_color};
            font-weight: bold;
        """)

    def enterEvent(self, event):
        self.setStyleSheet(f"""
            background-color: {button_hover_color};
            color: {bg_color};
            border-radius: 12px;
            padding: 10px 20px;
            border: 2px solid {button_hover_color};
            font-weight: bold;
        """)

    def leaveEvent(self, event):
        self.setStyleSheet(f"""
            background-color: {bg_color};
            color: white;
            border-radius: 12px;
            padding: 10px 20px;
            border: 2px solid {bg_color};
            font-weight: bold;
        """)

    def mousePressEvent(self, event):
        self.setStyleSheet(f"""
            background-color: {button_click_color};
            color: {bg_color};
            border-radius: 12px;
            padding: 10px 20px;
            border: 2px solid {button_click_color};
            font-weight: bold;
        """)
        super().mousePressEvent(event)
        self.function()

    def mouseReleaseEvent(self, event):
        self.enterEvent(event)
        super().mouseReleaseEvent(event)

class HoverTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            background-color: #ffffff;
            border: 2px solid #1B3A5E;
            padding: 10px;
            border-radius: 8px;
            font-size: 12pt;
        """)

    def enterEvent(self, event):
        self.setStyleSheet("""
            background-color: #ffffff;
            border: 2px solid #FFB800;
            padding: 10px;
            border-radius: 8px;
            font-size: 12pt;
        """)

    def leaveEvent(self, event):
        self.setStyleSheet("""
            background-color: #ffffff;
            border: 2px solid #1B3A5E;
            padding: 10px;
            border-radius: 8px;
            font-size: 12pt;
        """)

class HoverDateEdit(QDateEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            background-color: #ffffff;
            border: 2px solid #1B3A5E;
            padding: 10px;
            border-radius: 8px;
            font-size: 12pt;
        """)

    def enterEvent(self, event):
        self.setStyleSheet("""
            background-color: #ffffff;
            border: 2px solid #FFB800;
            padding: 10px;
            border-radius: 8px;
            font-size: 12pt;
        """)

    def leaveEvent(self, event):
        self.setStyleSheet("""
            background-color: #ffffff;
            border: 2px solid #1B3A5E;
            padding: 10px;
            border-radius: 8px;
            font-size: 12pt;
        """)

def exibir_erro(titulo, mensagem):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(titulo)
    msg.setText(mensagem)
    msg.setStyleSheet("background-color: #f7f7f7; color: black;")
    msg.exec()

def exibir_sucesso(titulo, mensagem):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setWindowTitle(titulo)
    msg.setText(mensagem)
    msg.setStyleSheet("background-color: #f7f7f7; color: black;")
    msg.exec()

def tela_testes(usuario_id):
    testes_window = QWidget()
    testes_window.setWindowTitle("Cadastro de POP")
    testes_window.setFixedSize(900, 750)
    testes_window.setStyleSheet("background-color: #f4f4f4; border-radius: 20px;")

    layout = QVBoxLayout()
    title_label = QLabel("Cadastro de POP (Procedimento Operacional Padrão)")
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_label.setFont(QFont("Arial", 22, QFont.Weight.Bold))
    title_label.setStyleSheet(f"color: {fg_color};")
    layout.addWidget(title_label)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setStyleSheet("""
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
    """)

    container_widget = QWidget()
    form_layout = QFormLayout()

    campos = [
        "Título do Procedimento", "Código do Documento", "Versão", "Data de Emissão",
        "Responsável", "Objetivo", "Aplicação e Escopo", "Responsabilidades",
        "Materiais e Equipamentos", "Preparação", "Operação", "Finalização",
        "Controle de Qualidade", "Seguranças e Riscos", "Manutenção e Calibração",
        "Referências", "Histórico de Revisões"
    ]

    entradas = {}
    for campo in campos:
        label = QLabel(f"{campo}:")
        label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        label.setStyleSheet(f"color: {bg_color};")
        if campo == "Data de Emissão":
            entradas[campo] = HoverDateEdit()
            entradas[campo].setDisplayFormat("dd/MM/yyyy")
            entradas[campo].setDate(QDate.currentDate())
        else:
            entradas[campo] = HoverTextEdit()
        form_layout.addRow(label, entradas[campo])

    container_widget.setLayout(form_layout)
    scroll_area.setWidget(container_widget)
    layout.addWidget(scroll_area)

    # Área de anexos e legendas múltiplas
    anexos_label = QLabel("Anexos e Legendas")
    anexos_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
    anexos_label.setStyleSheet(f"color: {bg_color}; margin-top:15px;")
    layout.addWidget(anexos_label)

    anexos_list = QListWidget()
    layout.addWidget(anexos_list)

    legenda_edits = []

    def adicionar_anexo():
        arquivos, _ = QFileDialog.getOpenFileNames(
            testes_window, "Selecionar arquivos", "", "Imagens (*.jpg *.jpeg *.png *.gif);;Todos os Arquivos (*)"
        )
        if arquivos:
            for arquivo in arquivos:
                item = QListWidgetItem(os.path.basename(arquivo))
                anexos_list.addItem(item)
                legenda_edit = QLineEdit()
                legenda_edit.setPlaceholderText("Digite aqui a legenda para a sua imagem")
                legenda_edits.append((arquivo, legenda_edit))
                # Criar layout temporário para legenda para colocar abaixo da lista
                layout.insertWidget(layout.count() - 3, legenda_edit)  # Insere antes dos botões

    def remover_anexo():
        selected_items = anexos_list.selectedItems()
        if not selected_items:
            exibir_erro("Erro", "Selecione um anexo para remover.")
            return
        for item in selected_items:
            idx = anexos_list.row(item)
            anexos_list.takeItem(idx)
            # Remover legenda associada
            arquivo, legenda_edit = legenda_edits.pop(idx)
            legenda_edit.deleteLater()

    caminho_imagens = []

    btn_add_anexo = HoverButton("Adicionar Anexo(s)", adicionar_anexo)
    btn_remove_anexo = HoverButton("Remover Anexo Selecionado", remover_anexo)
    layout.addWidget(btn_add_anexo)
    layout.addWidget(btn_remove_anexo)

    def salvar():
        valores = {
            "procedimento_operacional": "POP",
            "titulo_procedimento": entradas["Título do Procedimento"].toPlainText().strip(),
            "codigo_documento": entradas["Código do Documento"].toPlainText().strip(),
            "versao": entradas["Versão"].toPlainText().strip(),
            "data_emissao": entradas["Data de Emissão"].date().toString("dd/MM/yyyy"),
            "responsavel": entradas["Responsável"].toPlainText().strip(),
            "objetivo": entradas["Objetivo"].toPlainText().strip(),
            "aplicacao_escopo": entradas["Aplicação e Escopo"].toPlainText().strip(),
            "responsabilidades": entradas["Responsabilidades"].toPlainText().strip(),
            "materiais_equipamentos": entradas["Materiais e Equipamentos"].toPlainText().strip(),
            "preparacao": entradas["Preparação"].toPlainText().strip(),
            "operacao": entradas["Operação"].toPlainText().strip(),
            "finalizacao": entradas["Finalização"].toPlainText().strip(),
            "controle_qualidade": entradas["Controle de Qualidade"].toPlainText().strip(),
            "segurancas_riscos": entradas["Seguranças e Riscos"].toPlainText().strip(),
            "manutencao_calibracao": entradas["Manutenção e Calibração"].toPlainText().strip(),
            "referencias": entradas["Referências"].toPlainText().strip(),
            "historico_revisoes": entradas["Histórico de Revisões"].toPlainText().strip()
        }

        if any(not v for v in valores.values()):
            exibir_erro("Erro", "Todos os campos devem ser preenchidos.")
            return

        if not legenda_edits:
            exibir_erro("Erro", "Adicione ao menos um anexo com legenda.")
            return

        imagens = []
        legendas = []
        for arquivo, legenda_edit in legenda_edits:
            texto_legenda = legenda_edit.text().strip()
            if not texto_legenda:
                exibir_erro("Erro", f"Legenda vazia para a imagem {os.path.basename(arquivo)}.")
                return
            imagens.append(arquivo)
            legendas.append(texto_legenda)

        try:
            db.salvar_teste(usuario_id, **valores)
            modelo_path = "assets/pop_model.docx"
            if not os.path.exists(modelo_path):
                exibir_erro("Erro", "O modelo 'pop_model.docx' não foi encontrado na pasta 'assets'.")
                return

            doc_temp_path = preencher_pop(valores, modelo_path, imagens, legendas)
            destino, _ = QFileDialog.getSaveFileName(testes_window, "Salvar POP preenchido", f"{valores['codigo_documento']}_POP.docx", "Documentos Word (*.docx)")
            if destino:
                os.replace(doc_temp_path, destino)
                exibir_sucesso("Sucesso", "POP salvo com sucesso.")
        except Exception as e:
            exibir_erro("Erro ao salvar POP", str(e))

    def limpar_campos():
        confirmacao = QMessageBox.question(testes_window, "Confirmar Limpeza", "Você deseja apagar todos os campos?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmacao == QMessageBox.StandardButton.Yes:
            for campo, widget in entradas.items():
                if isinstance(widget, QTextEdit):
                    widget.clear()
                elif isinstance(widget, QDateEdit):
                    widget.setDate(QDate.currentDate())
            while anexos_list.count():
                anexos_list.takeItem(0)
            for _, legenda_edit in legenda_edits:
                legenda_edit.deleteLater()
            legenda_edits.clear()

    layout.addWidget(HoverButton("Salvar POP", salvar))
    layout.addWidget(HoverButton("Limpar Campos", limpar_campos))
    layout.addWidget(HoverButton("Voltar", lambda: (testes_window.close(), __import__('telas.tela_usuario').tela_usuario.tela_usuario(usuario_id))))
    testes_window.setLayout(layout)
    testes_window.show()
