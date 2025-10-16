from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget, QWidget, QTableWidget, QTableWidgetItem, QAbstractItemView, QLineEdit, QTextEdit, QDateEdit, QFormLayout, QDialogButtonBox, QMessageBox
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from db.db import get_process_header, list_process_activities, add_process_activity, update_process_activity, delete_process_activity

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
        d = self.dt.date().toString("yyyy-MM-dd")
        t = self.edt_title.text().strip()
        n = self.edt_note.toPlainText().strip()
        return d, t, n

class ProcessDetailDialog(QDialog):
    def __init__(self, process_id: int, parent=None):
        super().__init__(parent)
        self.process_id = process_id
        self.setWindowTitle(f"Detalhe do Processo #{process_id}")
        self.setMinimumSize(980, 640)
        self.setStyleSheet("""
            QDialog, QWidget { background-color: #0f172a; color: #e2e8f0; font-family: 'Segoe UI', sans-serif; }
            QLabel#title { color: #FFCD00; font-size: 20px; font-weight: bold; }
            QPushButton { background-color: #FFCD00; color: #0f172a; border: 0; padding: 10px 14px; border-radius: 8px; }
            QPushButton:hover { opacity: 0.9; }
            QTableWidget { background-color: #0b1220; gridline-color: #1e293b; }
            QHeaderView::section { background-color: #111827; color: #e2e8f0; padding: 6px; border: 0; }
            QLineEdit, QTextEdit { background: #0b1220; border: 1px solid #1e293b; padding: 8px; border-radius: 8px; }
            QDateEdit { background: #0b1220; border: 1px solid #1e293b; padding: 6px; border-radius: 8px; }
        """)
        root = QVBoxLayout()
        header = QHBoxLayout()
        self.lbl_title = QLabel("")
        self.lbl_title.setObjectName("title")
        header.addWidget(self.lbl_title)
        header.addStretch()
        root.addLayout(header)
        self.tabs = QTabWidget()
        self.tab_overview = QWidget()
        self.tab_activities = QWidget()
        self.tabs.addTab(self.tab_overview, "Visão Geral")
        self.tabs.addTab(self.tab_activities, "Atividades")
        root.addWidget(self.tabs)
        self.setLayout(root)
        self.setup_overview()
        self.setup_activities()
        self.load_overview()
        self.load_activities()

    def setup_overview(self):
        l = QVBoxLayout()
        self.lbl_overview = QLabel("")
        l.addWidget(self.lbl_overview)
        l.addStretch()
        self.tab_overview.setLayout(l)

    def load_overview(self):
        row = get_process_header(self.process_id)
        if row:
            _, title, code, phase, status, owner_id, start_date, due_date, closed_at, tags_json, created_at, updated_at = row
            self.lbl_title.setText(f"{title} • {code if code else ''}")
            txt = []
            txt.append(f"Título: {title}")
            txt.append(f"Código: {code or '-'}")
            txt.append(f"Fase: {phase or '-'}")
            txt.append(f"Status: {status or '-'}")
            txt.append(f"Responsável: {owner_id or '-'}")
            txt.append(f"Início: {start_date or '-'}")
            txt.append(f"Entrega: {due_date or '-'}")
            txt.append(f"Encerrado: {closed_at or '-'}")
            txt.append(f"Criado em: {created_at or '-'}")
            txt.append(f"Atualizado em: {updated_at or '-'}")
            self.lbl_overview.setText("\n".join(txt))
        else:
            self.lbl_title.setText("Processo não encontrado")
            self.lbl_overview.setText("")

    def setup_activities(self):
        l = QVBoxLayout()
        btns = QHBoxLayout()
        self.btn_add = QPushButton("Adicionar")
        self.btn_edit = QPushButton("Editar")
        self.btn_del = QPushButton("Excluir")
        btns.addWidget(self.btn_add)
        btns.addWidget(self.btn_edit)
        btns.addWidget(self.btn_del)
        btns.addStretch()
        l.addLayout(btns)
        self.tbl = QTableWidget(0, 6)
        self.tbl.setHorizontalHeaderLabels(["ID", "Data", "Título", "Nota", "Autor", "Criado"])
        self.tbl.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tbl.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tbl.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tbl.horizontalHeader().setStretchLastSection(True)
        l.addWidget(self.tbl)
        self.tab_activities.setLayout(l)
        self.btn_add.clicked.connect(self.on_add)
        self.btn_edit.clicked.connect(self.on_edit)
        self.btn_del.clicked.connect(self.on_delete)

    def load_activities(self):
        rows = list_process_activities(self.process_id)
        self.tbl.setRowCount(0)
        for r in rows:
            idx = self.tbl.rowCount()
            self.tbl.insertRow(idx)
            for c, v in enumerate(r[:6]):
                it = QTableWidgetItem("" if v is None else str(v))
                if c == 0:
                    it.setData(Qt.ItemDataRole.UserRole, r[0])
                self.tbl.setItem(idx, c, it)

    def current_activity_id(self):
        sel = self.tbl.selectedItems()
        if not sel:
            return None
        row = sel[0].row()
        it = self.tbl.item(row, 0)
        if not it:
            return None
        return it.data(Qt.ItemDataRole.UserRole)

    def on_add(self):
        dlg = ActivityForm(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            d, t, n = dlg.values()
            if not t or not d:
                QMessageBox.warning(self, "Atenção", "Preencha data e título.")
                return
            add_process_activity(self.process_id, d, t, n, None)
            self.load_activities()

    def on_edit(self):
        aid = self.current_activity_id()
        if not aid:
            QMessageBox.information(self, "Info", "Selecione uma atividade.")
            return
        row = self.tbl.currentRow()
        d0 = self.tbl.item(row, 1).text()
        t0 = self.tbl.item(row, 2).text()
        n0 = self.tbl.item(row, 3).text()
        qd = QDate.fromString(d0, "yyyy-MM-dd")
        dlg = ActivityForm(self, qd, t0, n0)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            d, t, n = dlg.values()
            if not t or not d:
                QMessageBox.warning(self, "Atenção", "Preencha data e título.")
                return
            update_process_activity(aid, d, t, n)
            self.load_activities()

    def on_delete(self):
        aid = self.current_activity_id()
        if not aid:
            QMessageBox.information(self, "Info", "Selecione uma atividade.")
            return
        ret = QMessageBox.question(self, "Confirmação", "Excluir atividade selecionada?")
        if ret == QMessageBox.StandardButton.Yes:
            delete_process_activity(aid)
            self.load_activities()
