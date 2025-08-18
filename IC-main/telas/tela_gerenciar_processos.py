from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QSpacerItem, QSizePolicy, QLineEdit
from PyQt6.QtCore import Qt
from db.db import listar_processos, salvar_processo

class TelaGerenciarProcessos(QWidget):
    def __init__(self, usuario_id=None):
        super().__init__()
        self.usuario_id = usuario_id
        self.build_ui()
        self.carregar_tabela_processos()

    def build_ui(self):
        self.setObjectName("TelaGerenciarProcessos")
        main = QVBoxLayout(self)
        header = QHBoxLayout()
        self.btn_criar = QPushButton("+ Criar")
        self.btn_criar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_criar.clicked.connect(self.on_create)
        self.btn_detalhes = QPushButton("Detalhes")
        self.btn_detalhes.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_dashboard.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_relatorio = QPushButton("Gerar Relatório")
        self.btn_relatorio.setCursor(Qt.CursorShape.PointingHandCursor)
        header.addWidget(self.btn_criar)
        header.addWidget(self.btn_detalhes)
        header.addWidget(self.btn_dashboard)
        header.addWidget(self.btn_relatorio)
        header.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main.addLayout(header)
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Nome do Processo", "Iniciado em", "Ações"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)
        main.addWidget(self.table)
        footer = QHBoxLayout()
        self.btn_voltar = QPushButton("← Voltar")
        self.btn_voltar.setCursor(Qt.CursorShape.PointingHandCursor)
        footer.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        footer.addWidget(self.btn_voltar)
        main.addLayout(footer)

    def _fmt_dt(self, dt):
        if not dt:
            return ""
        try:
            y, m, d = dt[0:4], dt[5:7], dt[8:10]
            hh, mm = dt[11:13], dt[14:16]
            return f"{d}/{m}/{y} {hh}:{mm}"
        except:
            return dt

    def carregar_tabela_processos(self):
        rows = listar_processos()
        self.table.setRowCount(0)
        for pid, nome, descricao, padrao, created_at in rows:
            r = self.table.rowCount()
            self.table.insertRow(r)
            item_nome = QTableWidgetItem(nome or "")
            item_nome.setData(Qt.ItemDataRole.UserRole, pid)
            self.table.setItem(r, 0, item_nome)
            self.table.setItem(r, 1, QTableWidgetItem(self._fmt_dt(created_at)))
            btn = QPushButton("Detalhes")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, x=pid: self.on_details(x))
            self.table.setCellWidget(r, 2, btn)
        self.table.resizeColumnsToContents()

    def on_create(self):
        nome = self._prompt_nome()
        if not nome:
            return
        salvar_processo(nome)
        self.carregar_tabela_processos()
        QMessageBox.information(self, "Processos", "Processo criado com sucesso.")

    def _prompt_nome(self):
        box = QMessageBox(self)
        box.setWindowTitle("Novo Processo")
        box.setText("Digite o nome do processo:")
        line = QLineEdit(box)
        box.layout().addWidget(line, 1, 1)
        box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        res = box.exec()
        if res == QMessageBox.StandardButton.Ok:
            t = line.text().strip()
            return t if t else None
        return None

    def on_details(self, pid: int):
        QMessageBox.information(self, "Detalhes", f"Detalhes do processo #{pid}")
