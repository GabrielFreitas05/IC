from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget, QWidget,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QLineEdit, QTextEdit, QDateEdit,
    QFormLayout, QDialogButtonBox, QMessageBox, QHeaderView, QFileDialog, QFrame
)
from PyQt6.QtCore import Qt, QDate
from fpdf import FPDF
from datetime import datetime

from db.db import (
    list_process_activities,
    add_process_activity,
    update_process_activity,
    delete_process_activity,
    conectar,
)


# -------------------- Formulário de atividade --------------------
class ActivityForm(QDialog):
    def __init__(self, parent=None, entry_date=None, title="", note=""):
        super().__init__(parent)
        self.setWindowTitle("Atividade")
        layout = QVBoxLayout()
        form = QFormLayout()

        self.dt = QDateEdit()
        self.dt.setCalendarPopup(True)
        self.dt.setDate(entry_date if entry_date else QDate.currentDate())
        self.edt_title = QLineEdit(title)
        self.edt_note = QTextEdit()
        self.edt_note.setPlainText(note or "")

        form.addRow("Data", self.dt)
        form.addRow("Título", self.edt_title)
        form.addRow("Nota", self.edt_note)
        layout.addLayout(form)

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)
        self.setLayout(layout)

    def values(self):
        # salvar no banco em yyyy-mm-dd
        d = self.dt.date().toString("yyyy-MM-dd")
        t = self.edt_title.text().strip()
        n = self.edt_note.toPlainText().strip()
        return d, t, n


# -------------------- Tela de Detalhes --------------------
class TelaDetalhesProcessos(QDialog):
    """
    Vinculado a formularios_processos.id
    A timeline (process_activities.process_id) referencia formularios_processos(id).
    """
    def __init__(self, process_id: int, parent=None):
        super().__init__(parent)
        self.process_id = process_id
        self.setWindowTitle(f"Detalhe do Processo #{process_id}")
        self.setMinimumSize(1000, 720)

        # ====== THEME / STYLESHEET ======
        BG            = "#0b1220"
        SURFACE       = "#0f172a"
        SURFACE_SOFT  = "#111827"
        BORDER        = "#1e293b"
        TEXT          = "#e2e8f0"
        ACCENT        = "#FFCD00"
        ACCENT_HOVER  = "#e6b800"
        DANGER        = "#ef4444"

        self.setStyleSheet(f"""
            QDialog, QWidget {{
                background-color: {BG};
                color: {TEXT};
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }}
            QLabel#title {{
                color: {ACCENT};
                font-size: 22px;
                font-weight: 700;
                letter-spacing: .5px;
            }}

            QPushButton {{
                background-color: {ACCENT};
                color: #0f172a;
                border: 0;
                padding: 10px 16px;
                border-radius: 10px;
                font-weight: 600;
            }}
            QPushButton:hover {{ background-color: {ACCENT_HOVER}; }}
            QPushButton:disabled {{ background: #404959; color: #aab3c2; }}
            QPushButton[variant="secondary"] {{
                background: {SURFACE_SOFT};
                color: {TEXT};
                border: 1px solid {BORDER};
            }}
            QPushButton[variant="secondary"]:hover {{ background: #162235; }}
            QPushButton[variant="danger"] {{ background: {DANGER}; color: white; }}
            QPushButton[variant="danger"]:hover {{ background: #dc2626; }}

            QTabWidget::pane {{
                border: 1px solid {BORDER};
                background: {SURFACE};
                border-radius: 12px;
                top: -1px;
            }}
            QTabBar {{ qproperty-drawBase: 0; }}
            QTabBar::tab {{
                background: {SURFACE_SOFT};
                color: {TEXT};
                padding: 8px 18px;
                border: 1px solid {BORDER};
                border-bottom: none;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                margin-right: 6px;
            }}
            QTabBar::tab:hover {{ background: #1a2942; }}
            QTabBar::tab:selected {{
                background: {ACCENT};
                color: #0f172a;
                border-color: {ACCENT};
            }}
            QTabBar::tab:!selected {{ margin-top: 4px; }}

            QLineEdit, QTextEdit, QDateEdit {{
                background: {SURFACE};
                border: 1px solid {BORDER};
                padding: 8px 10px;
                border-radius: 10px;
                selection-background-color: {ACCENT};
                selection-color: #0f172a;
            }}

            QTableWidget {{
                background: {SURFACE};
                gridline-color: {BORDER};
                border: 1px solid {BORDER};
                border-radius: 12px;
                alternate-background-color: #0c1526;
            }}
            QHeaderView::section {{
                background: {SURFACE_SOFT};
                color: {TEXT};
                padding: 10px 8px;
                border: none;
                font-weight: 600;
                border-right: 1px solid {BORDER};
            }}
            QTableWidget::item:selected {{
                background: {ACCENT};
                color: #0f172a;
            }}

            QScrollBar:vertical {{
                background: transparent; width: 12px; margin: 12px 0 12px 0;
            }}
            QScrollBar::handle:vertical {{
                background: #263246; min-height: 32px; border-radius: 6px;
            }}
            QScrollBar::handle:vertical:hover {{ background: #2d3a50; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
            QScrollBar:horizontal {{
                background: transparent; height: 12px; margin: 0 12px;
            }}
            QScrollBar::handle:horizontal {{
                background: #263246; min-width: 32px; border-radius: 6px;
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
        """)

        # ====== LAYOUT ======
        root = QVBoxLayout()
        header = QHBoxLayout()
        self.lbl_title = QLabel("")
        self.lbl_title.setObjectName("title")
        header.addWidget(self.lbl_title)
        header.addStretch()

        self.btn_exportar = QPushButton("🖨️ Exportar PDF")
        header.addWidget(self.btn_exportar)

        root.addLayout(header)

        # Card container para as tabs
        card = QFrame()
        card.setObjectName("card")
        card.setStyleSheet("""
            QFrame#card {
                background: #0f172a;
                border: 1px solid #1e293b;
                border-radius: 14px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(12, 12, 12, 12)

        self.tabs = QTabWidget()
        self.tab_overview = QWidget()
        self.tab_activities = QWidget()
        self.tabs.addTab(self.tab_overview, "Visão Geral")
        self.tabs.addTab(self.tab_activities, "Atividades")

        card_layout.addWidget(self.tabs)
        root.addWidget(card)
        self.setLayout(root)

        # conexões
        self.btn_exportar.clicked.connect(self._on_export_pdf)

        self._setup_overview()
        self._setup_activities()
        self._load_overview()
        self._load_activities()

    # -------- Visão geral --------
    def _setup_overview(self):
        l = QVBoxLayout()
        self.lbl_overview = QLabel("")
        self.lbl_overview.setAlignment(Qt.AlignmentFlag.AlignTop)
        l.addWidget(self.lbl_overview)
        l.addStretch()
        self.tab_overview.setLayout(l)

    def _load_overview(self):
        self._overview_row = None
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                SELECT id, nome_processo, responsavel, data_inicio, nome_fase, objetivo_fase, data_registro
                FROM formularios_processos
                WHERE id = ?
            """, (self.process_id,))
            row = cur.fetchone()
            self._overview_row = row
        finally:
            if 'conn' in locals():
                conn.close()

        if self._overview_row:
            pid, nome, responsavel, data_inicio, nome_fase, objetivo_fase, data_registro = self._overview_row

            # data início dd/mm/yyyy
            try:
                data_inicio_formatada = datetime.strptime(data_inicio, "%Y-%m-%d").strftime("%d/%m/%Y") if data_inicio else "-"
            except Exception:
                data_inicio_formatada = data_inicio or "-"

            try:
                data_registro_formatada = datetime.strptime(data_registro, "%Y-%m-%d").strftime("%d/%m/%Y") if data_registro else "-"
            except Exception:
                data_registro_formatada = data_registro or "-"

            self.lbl_title.setText(f"{(nome or '').upper()}  •  ID {pid}")
            texto = [
                f"Nome: {nome or '-'}",
                f"Responsável: {responsavel or '-'}",
                f"Início: {data_inicio_formatada}",
                f"Fase: {nome_fase or '-'}",
                f"Objetivo da Fase: {objetivo_fase or '-'}",
                f"Registrado em: {data_registro_formatada}",
            ]
            self.lbl_overview.setText("\n".join(texto))
        else:
            self.lbl_title.setText("Processo não encontrado")
            self.lbl_overview.setText("")

    # -------- Atividades --------
    def _setup_activities(self):
        l = QVBoxLayout()
        btns = QHBoxLayout()

        self.btn_add = QPushButton("Adicionar")
        self.btn_add.setProperty("variant", "secondary")
        self.btn_edit = QPushButton("Editar")
        self.btn_edit.setProperty("variant", "secondary")
        self.btn_del = QPushButton("Excluir")
        self.btn_del.setProperty("variant", "danger")

        btns.addWidget(self.btn_add)
        btns.addWidget(self.btn_edit)
        btns.addWidget(self.btn_del)
        btns.addStretch()
        l.addLayout(btns)

        # Agora SEM a coluna ID visível
        self.tbl = QTableWidget(0, 5)
        self.tbl.setHorizontalHeaderLabels(["Data", "Título", "Nota", "Autor", "Criado em"])
        self.tbl.verticalHeader().setVisible(False)
        self.tbl.setAlternatingRowColors(True)
        self.tbl.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tbl.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        header = self.tbl.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Data
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)           # Título
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)           # Nota
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Autor
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Criado em

        l.addWidget(self.tbl)
        self.tab_activities.setLayout(l)

        self.btn_add.clicked.connect(self._on_add)
        self.btn_edit.clicked.connect(self._on_edit)
        self.btn_del.clicked.connect(self._on_delete)

    def _load_activities(self):
        rows = list_process_activities(self.process_id)  # cada r = (id, entry_date, title, note, author, created_at)
        self._activities = rows
        self.tbl.setRowCount(0)
        for r in rows:
            a_id, a_date, a_title, a_note, a_author, a_created = r[:6]

            # formatos bonitos
            try:
                a_date_fmt = datetime.strptime(a_date, "%Y-%m-%d").strftime("%d/%m/%Y") if a_date else "-"
            except Exception:
                a_date_fmt = a_date or "-"
            try:
                a_created_fmt = datetime.strptime(a_created, "%Y-%m-%d").strftime("%d/%m/%Y") if a_created else "-"
            except Exception:
                a_created_fmt = a_created or "-"

            idx = self.tbl.rowCount()
            self.tbl.insertRow(idx)

            # guardamos o id da atividade como UserRole na primeira coluna (Data)
            it_date = QTableWidgetItem(a_date_fmt)
            it_date.setData(Qt.ItemDataRole.UserRole, a_id)
            it_title = QTableWidgetItem(a_title or "-")
            it_note  = QTableWidgetItem(a_note or "-")
            it_author= QTableWidgetItem(a_author or "-")
            it_created = QTableWidgetItem(a_created_fmt)

            # alinhamentos
            it_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            it_created.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.tbl.setItem(idx, 0, it_date)
            self.tbl.setItem(idx, 1, it_title)
            self.tbl.setItem(idx, 2, it_note)
            self.tbl.setItem(idx, 3, it_author)
            self.tbl.setItem(idx, 4, it_created)

    def _current_activity_id(self):
        sel = self.tbl.selectedItems()
        if not sel:
            return None
        row = sel[0].row()
        it = self.tbl.item(row, 0)  # coluna "Data" guarda o ID em UserRole
        if not it:
            return None
        return it.data(Qt.ItemDataRole.UserRole)

    def _on_add(self):
        dlg = ActivityForm(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            d, t, n = dlg.values()
            if not t or not d:
                QMessageBox.warning(self, "Atenção", "Preencha data e título.")
                return
            add_process_activity(self.process_id, d, t, n, None)
            self._load_activities()

    def _on_edit(self):
        aid = self._current_activity_id()
        if not aid:
            QMessageBox.information(self, "Info", "Selecione uma atividade.")
            return
        row = self.tbl.currentRow()
        # converter de volta 'dd/mm/yyyy' para QDate
        d0_txt = self.tbl.item(row, 0).text()
        try:
            qd = QDate.fromString(d0_txt, "dd/MM/yyyy")
            if not qd.isValid():
                raise ValueError
        except Exception:
            qd = QDate.currentDate()
        t0 = self.tbl.item(row, 1).text()
        n0 = self.tbl.item(row, 2).text()

        dlg = ActivityForm(self, qd, t0, n0)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            d, t, n = dlg.values()
            if not t or not d:
                QMessageBox.warning(self, "Atenção", "Preencha data e título.")
                return
            update_process_activity(aid, d, t, n)
            self._load_activities()

    def _on_delete(self):
        aid = self._current_activity_id()
        if not aid:
            QMessageBox.information(self, "Info", "Selecione uma atividade.")
            return
        ret = QMessageBox.question(self, "Confirmação", "Excluir atividade selecionada?")
        if ret == QMessageBox.StandardButton.Yes:
            delete_process_activity(aid)
            self._load_activities()

    # -------- Exportar PDF (sem mostrar ID do processo, e tabela sem coluna ID) --------
    def _on_export_pdf(self):
        if not self._overview_row:
            QMessageBox.warning(self, "Aviso", "Cabeçalho do processo não carregado.")
            return

        pid, nome, responsavel, data_inicio, nome_fase, objetivo_fase, data_registro = self._overview_row

        # Formatação das datas do cabeçalho
        try:
            data_inicio_formatada = datetime.strptime(data_inicio, "%Y-%m-%d").strftime("%d/%m/%Y") if data_inicio else "-"
        except Exception:
            data_inicio_formatada = data_inicio or "-"
        try:
            data_registro_formatada = datetime.strptime(data_registro, "%Y-%m-%d").strftime("%d/%m/%Y") if data_registro else "-"
        except Exception:
            data_registro_formatada = data_registro or "-"

        default_name = f"Processo_{(nome or '').strip().replace(' ', '_')}.pdf"
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar PDF do Processo", default_name, "PDF Files (*.pdf)")
        if not file_path:
            return

        try:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            # Título
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Relatório do Processo", ln=True, align="C")
            pdf.ln(4)

            # Cabeçalho (sem mostrar ID do processo para o usuário)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, f"Processo: {nome or '-'}", ln=True)
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 8, f"Responsável: {responsavel or '-'}", ln=True)
            pdf.cell(0, 8, f"Início: {data_inicio_formatada}", ln=True)
            pdf.cell(0, 8, f"Fase: {nome_fase or '-'}", ln=True)
            pdf.multi_cell(0, 8, f"Objetivo da Fase: {objetivo_fase or '-'}")
            pdf.cell(0, 8, f"Registrado em: {data_registro_formatada}", ln=True)
            pdf.ln(4)

            # Atividades (sem coluna ID)
            pdf.set_font("Arial", "B", 13)
            pdf.cell(0, 9, "Atividades pós criação", ln=True)
            pdf.ln(2)
            pdf.set_font("Arial", "B", 11)
            col_w = [35, 55, 0]
            pdf.cell(col_w[0], 8, "Data", border=1)
            pdf.cell(col_w[1], 8, "Título", border=1)
            pdf.cell(col_w[2], 8, "Nota", border=1, ln=True)

            pdf.set_font("Arial", "", 11)
            for r in (self._activities or []):
                a_id, a_date, a_title, a_note, a_author, a_created = r[:6]
                try:
                    a_date_fmt = datetime.strptime(a_date, "%Y-%m-%d").strftime("%d/%m/%Y") if a_date else "-"
                except Exception:
                    a_date_fmt = a_date or "-"

                pdf.cell(col_w[0], 8, a_date_fmt, border=1)
                pdf.cell(col_w[1], 8, str(a_title or "-"), border=1)
                pdf.multi_cell(col_w[2], 8, str(a_note or "-"), border=1)

            # salvar
            try:
                pdf.output(file_path)
                QMessageBox.information(self, "Sucesso", f"PDF gerado em:\n{file_path}")
            except PermissionError:
                QMessageBox.warning(self, "Aviso", "O arquivo está aberto ou bloqueado.\nFeche o PDF e tente novamente com outro nome.")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao gerar PDF:\n{str(e)}")

