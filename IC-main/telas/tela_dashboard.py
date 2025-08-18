from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class TelaDashboard(QWidget):
    def __init__(self, process_id=None):
        super().__init__()
        self.current_process_id = process_id
        self.setMinimumSize(800, 500)
        root = QVBoxLayout(self)
        title = QLabel("Dashboard")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 18))
        root.addWidget(title)
        self.info = QLabel("")
        self.info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info.setFont(QFont("Segoe UI", 12))
        root.addWidget(self.info, 1)
        self._update_label()

    def _update_label(self):
        if self.current_process_id:
            self.info.setText(f"Exibindo dados do processo ID {self.current_process_id}")
        else:
            self.info.setText("Selecione um processo para visualizar")

    def set_process(self, process_id):
        self.current_process_id = process_id
        self._update_label()

    def refresh(self):
        self._update_label()
