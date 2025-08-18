from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QDateEdit, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView, QAbstractItemView, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt, QDate
from db.db import salvar_pta_db, listar_ptas_por_usuario_db, atualizar_pta_db, excluir_pta_db, buscar_nome_usuario

BG_COLOR = "#1B3A5E"
FG_COLOR = "#FFCD00"
INPUT_BG_COLOR = "#FFFFFF"
INPUT_BORDER_COLOR = "#1B3A5E"
INPUT_BORDER_HOVER = "#FFB800"
BUTTON_HOVER = "#FFB800"
BUTTON_CLICK = "#FF8000"

class HoverButton(QPushButton):
    def __init__(self, text, function=None):
        super().__init__(text)
        self.function = function
        self.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {FG_COLOR};
                color: {BG_COLOR};
                border-radius: 10px;
                padding: 10px 20px;
                border: none;
                min-width: 140px;
            }}
            QPushButton:hover {{
                background-color: {BUTTON_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {BUTTON_CLICK};
            }}
        """)
        if self.function:
            self.clicked.connect(self.function)

class CustomTextEdit(QTextEdit):
    def __init__(self, placeholder_text=""):
        super().__init__()
        self.placeholder_text = placeholder_text
        self.setFont(QFont("Segoe UI", 10))
        self._set_default_style()
        self.focusInEvent = self._handle_focus_in
        self.focusOutEvent = self._handle_focus_out
        self._set_placeholder()

    def _set_default_style(self):
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {INPUT_BG_COLOR};
                color: #333333;
                border: 1.5px solid {INPUT_BORDER_COLOR};
                border-radius: 8px;
                padding: 8px;
                font-size: 12pt;
            }}
        """)

    def _set_focus_style(self):
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {INPUT_BG_COLOR};
                color: #333333;
                border: 1.7px solid {INPUT_BORDER_HOVER};
                border-radius: 8px;
                padding: 8px;
                font-size: 12pt;
            }}
        """)

    def _set_placeholder(self):
        if not self.toPlainText() and self.placeholder_text:
            self.setText(self.placeholder_text)
            pal = self.palette()
            pal.setColor(self.viewport().foregroundRole(), QColor('gray'))
            self.setPalette(pal)
        else:
            pal = self.palette()
            pal.setColor(self.viewport().foregroundRole(), QColor('#333333'))
            self.setPalette(pal)

    def _handle_focus_in(self, event):
        self._set_focus_style()
        if self.toPlainText() == self.placeholder_text:
            self.clear()
        super().focusInEvent(event)

    def _handle_focus_out(self, event):
        if not self.toPlainText():
            self._set_placeholder()
        self._set_default_style()
        super().focusOutEvent(event)

    def text(self):
        content = self.toPlainText()
        return "" if content == self.placeholder_text else content

class CustomDateEdit(QDateEdit):
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Segoe UI", 11))
        self.setCalendarPopup(True)
        self.setDate(QDate.currentDate())
        self.setStyleSheet(f"""
            QDateEdit {{
                background-color: {INPUT_BG_COLOR};
                border: 1.5px solid {INPUT_BORDER_COLOR};
                border-radius: 8px;
                padding: 8px;
                font-size: 12pt;
                color: #333333;
            }}
            QDateEdit:hover {{
                border: 1.7px solid {INPUT_BORDER_HOVER};
            }}
            QDateEdit::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid {INPUT_BORDER_COLOR};
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }}
            QDateEdit::down-arrow {{
                image: url(assets/icon_calendar.png);
                width: 14px;
                height: 14px;
            }}
        """)

class tela_pta(QWidget):
    def __init__(self, usuario_id, parent=None):
        super().__init__(parent)
        self.usuario_id = usuario_id
        self.pta_editando_id = None

        self.setWindowTitle("PTA - Planejamento Técnico de Atividades")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(f"background-color: {BG_COLOR};")

        self._setup_ui()
        self._carregar_ptas()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)

        nome_usuario = buscar_nome_usuario(self.usuario_id)
        title = QLabel(f"Planejamento Técnico de Atividades (PTA) - {nome_usuario}")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {FG_COLOR};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        h_layout = QHBoxLayout()
        h_layout.setSpacing(20)

        form_container = QWidget()
        form_container.setStyleSheet(f"background-color: {INPUT_BG_COLOR}; border-radius: 12px;")
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(18)

        lbl_data = QLabel("Data da Atividade:")
        lbl_data.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
        lbl_data.setStyleSheet(f"color: {BG_COLOR};")
        form_layout.addWidget(lbl_data)

        self.data_edit = CustomDateEdit()
        form_layout.addWidget(self.data_edit)

        lbl_desc = QLabel("Descrição da Atividade:")
        lbl_desc.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
        lbl_desc.setStyleSheet(f"color: {BG_COLOR};")
        form_layout.addWidget(lbl_desc)

        self.desc_edit = CustomTextEdit("Descreva a atividade planejada aqui...")
        self.desc_edit.setMinimumHeight(150)
        form_layout.addWidget(self.desc_edit)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        self.btn_salvar = HoverButton("Salvar PTA", self._salvar_ou_atualizar_pta)
        self.btn_limpar = HoverButton("Limpar Campos", self._limpar_formulario)
        btn_layout.addWidget(self.btn_salvar)
        btn_layout.addWidget(self.btn_limpar)
        form_layout.addLayout(btn_layout)

        h_layout.addWidget(form_container, 1)

        table_container = QWidget()
        table_container.setStyleSheet(f"background-color: {INPUT_BG_COLOR}; border-radius: 12px;")
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(20, 20, 20, 20)
        table_layout.setSpacing(15)

        lbl_table_title = QLabel("PTAs Registrados")
        lbl_table_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        lbl_table_title.setStyleSheet(f"color: {BG_COLOR};")
        table_layout.addWidget(lbl_table_title)

        self.tabela_ptas = QTableWidget()
        self.tabela_ptas.setColumnCount(3)
        self.tabela_ptas.setHorizontalHeaderLabels(["ID", "Data", "Descrição"])
        self.tabela_ptas.verticalHeader().setVisible(False)
        self.tabela_ptas.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabela_ptas.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabela_ptas.setAlternatingRowColors(True)
        self.tabela_ptas.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                border: 1px solid {BG_COLOR};
                border-radius: 8px;
                font-size: 11pt;
            }}
            QHeaderView::section {{
                background-color: {BG_COLOR};
                color: {FG_COLOR};
                padding: 8px;
                font-weight: bold;
                font-size: 11pt;
            }}
            QTableWidget::item:selected {{
                background-color: {FG_COLOR};
                color: {BG_COLOR};
            }}
        """)
        self.tabela_ptas.setColumnHidden(0, True)
        header = self.tabela_ptas.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        self.tabela_ptas.itemSelectionChanged.connect(self._carregar_pta_selecionado)

        table_layout.addWidget(self.tabela_ptas)

        tbl_btn_layout = QHBoxLayout()
        tbl_btn_layout.setSpacing(15)
        self.btn_editar = HoverButton("Editar Selecionado", self._editar_pta_selecionado)
        self.btn_excluir = HoverButton("Excluir Selecionado", self._excluir_pta_selecionado)
        tbl_btn_layout.addStretch()
        tbl_btn_layout.addWidget(self.btn_editar)
        tbl_btn_layout.addWidget(self.btn_excluir)
        table_layout.addLayout(tbl_btn_layout)

        h_layout.addWidget(table_container, 2)

        main_layout.addLayout(h_layout)

        spacer = QSpacerItem(20, 25, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        main_layout.addSpacerItem(spacer)

        self.btn_voltar = HoverButton("Voltar")
        self.btn_voltar.clicked.connect(self._voltar_tela_usuario)
        self.btn_voltar.setFixedWidth(140)
        main_layout.addWidget(self.btn_voltar, alignment=Qt.AlignmentFlag.AlignRight)

    def _carregar_ptas(self):
        self.tabela_ptas.setRowCount(0)
        ptas = listar_ptas_por_usuario_db(self.usuario_id)
        if ptas:
            for idx, pta in enumerate(ptas):
                self.tabela_ptas.insertRow(idx)
                self.tabela_ptas.setItem(idx, 0, QTableWidgetItem(str(pta[0])))
                self.tabela_ptas.setItem(idx, 1, QTableWidgetItem(pta[2]))
                self.tabela_ptas.setItem(idx, 2, QTableWidgetItem(pta[3]))
        self._limpar_formulario()

    def _limpar_formulario(self):
        self.data_edit.setDate(QDate.currentDate())
        self.desc_edit.clear()
        self.desc_edit._set_placeholder()
        self.pta_editando_id = None
        self.btn_salvar.setText("Salvar PTA")

    def _salvar_ou_atualizar_pta(self):
        data = self.data_edit.date().toString("yyyy-MM-dd")
        descricao = self.desc_edit.text().strip()

        if not descricao:
            QMessageBox.warning(self, "Erro", "A descrição da atividade não pode estar vazia.")
            return

        if self.pta_editando_id is None:
            sucesso = salvar_pta_db(self.usuario_id, data, descricao)
            if sucesso:
                QMessageBox.information(self, "Sucesso", "PTA salvo com sucesso!")
            else:
                QMessageBox.critical(self, "Erro", "Erro ao salvar PTA.")
        else:
            sucesso = atualizar_pta_db(self.pta_editando_id, data, descricao)
            if sucesso:
                QMessageBox.information(self, "Sucesso", "PTA atualizado com sucesso!")
            else:
                QMessageBox.critical(self, "Erro", "Erro ao atualizar PTA.")

        self._carregar_ptas()

    def _carregar_pta_selecionado(self):
        selected = self.tabela_ptas.selectedItems()
        if selected and len(selected) >= 3:
            pta_id = int(selected[0].text())
            data = selected[1].text()
            descricao = selected[2].text()
            self.pta_editando_id = pta_id
            self.data_edit.setDate(QDate.fromString(data, "yyyy-MM-dd"))
            self.desc_edit.setText(descricao)
            self.btn_salvar.setText("Atualizar PTA")
        else:
            self._limpar_formulario()

    def _editar_pta_selecionado(self):
        if self.pta_editando_id is None:
            QMessageBox.warning(self, "Aviso", "Selecione um PTA para editar primeiro.")
        else:
            self.data_edit.setFocus()

    def _excluir_pta_selecionado(self):
        if self.pta_editando_id is None:
            QMessageBox.warning(self, "Aviso", "Selecione um PTA para excluir.")
            return

        resp = QMessageBox.question(self, "Confirmar exclusão",
                                    "Tem certeza que deseja excluir o PTA selecionado?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if resp == QMessageBox.StandardButton.Yes:
            sucesso = excluir_pta_db(self.pta_editando_id)
            if sucesso:
                QMessageBox.information(self, "Sucesso", "PTA excluído com sucesso!")
            else:
                QMessageBox.critical(self, "Erro", "Erro ao excluir PTA.")
            self._carregar_ptas()

    def _voltar_tela_usuario(self):
        from telas.tela_usuario import tela_usuario
        self.close()
        tela_usuario(self.usuario_id)

