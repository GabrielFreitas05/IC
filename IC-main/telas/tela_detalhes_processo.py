from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from db.db import conectar

class TelaDetalhesProcesso(QWidget):
    deve_retornar = pyqtSignal()
    def __init__(self, usuario_id, processo_id):
        super().__init__()
        self.usuario_id = usuario_id
        self.processo_id = processo_id
        self.setWindowTitle("Detalhes do Processo")
        self.setFixedSize(900, 700)
        self.setStyleSheet("""
            QWidget { background-color: #1B3A5E; color: white; font-family: 'Segoe UI'; }
            QLabel { color: #FFCD00; }
            QPushButton { background-color: #FFCD00; color: #1B3A5E; font-weight: bold; border: none; padding: 10px 14px; border-radius: 6px; }
            QPushButton:hover { background-color: #e6b800; }
            QTableWidget { background-color: white; color: black; border-radius: 8px; font-size: 11pt; }
            QHeaderView::section { background-color: #1A2A47; color: #FFCD00; padding: 8px; font-weight: bold; font-size: 11pt; }
        """)
        self._setup_ui()
        self._carregar_detalhes()

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24,24,24,24)
        root.setSpacing(16)

        title = QLabel("Detalhes do Processo")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont('Segoe UI', 18))
        root.addWidget(title)

        self.lbl_nome = QLabel("")
        self.lbl_resp = QLabel("")
        self.lbl_inicio = QLabel("")
        info = QVBoxLayout()
        info.addWidget(self.lbl_nome)
        info.addWidget(self.lbl_resp)
        info.addWidget(self.lbl_inicio)
        root.addLayout(info)

        actions = QHBoxLayout()
        self.btn_add = QPushButton("Adicionar atualização")
        self.btn_finish = QPushButton("Terminar processo")
        self.btn_voltar = QPushButton("← Voltar")
        self.btn_add.clicked.connect(self._nao_implementado)
        self.btn_finish.clicked.connect(self._nao_implementado)
        self.btn_voltar.clicked.connect(lambda: self.deve_retornar.emit())
        actions.addWidget(self.btn_add)
        actions.addWidget(self.btn_finish)
        actions.addStretch()
        actions.addWidget(self.btn_voltar)
        root.addLayout(actions)

        self.tbl_timeline = QTableWidget()
        self.tbl_timeline.setColumnCount(3)
        self.tbl_timeline.setHorizontalHeaderLabels(["Data/Hora", "Tipo", "Descrição"])
        header = self.tbl_timeline.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        root.addWidget(self.tbl_timeline, 1)

    def _carregar_detalhes(self):
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("SELECT nome_processo, responsavel, strftime('%d/%m/%Y %H:%M', data_inicio) FROM formularios_processos WHERE id=?", (self.processo_id,))
            r = cur.fetchone()
            if r:
                self.lbl_nome.setText(f"Nome: {r[0] or ''}")
                self.lbl_resp.setText(f"Responsável: {r[1] or ''}")
                self.lbl_inicio.setText(f"Iniciado em: {r[2] or ''}")
            self.tbl_timeline.setRowCount(0)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar detalhes:\n{str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def _nao_implementado(self):
        QMessageBox.information(self, "Info", "Funcionalidade a implementar: registro de atualização e término.")
