# ui/components.py
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt

class HeaderBar(QWidget):
    def __init__(self, title: str, actions: list[QPushButton] | None = None, parent=None):
        super().__init__(parent)
        self.setObjectName("HeaderBar")
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        self.lbl = QLabel(title)
        self.lbl.setObjectName("title")
        lay.addWidget(self.lbl)
        lay.addStretch()
        for btn in (actions or []):
            lay.addWidget(btn)

class Card(QFrame):
    def __init__(self, parent=None, margin=12):
        super().__init__(parent)
        self.setObjectName("Card")
        self.setProperty("class", "Card")
        self.setStyleSheet("")  # classe é aplicada via stylesheet global
        self.lay = QVBoxLayout(self)
        self.lay.setContentsMargins(margin, margin, margin, margin)
        self.lay.setSpacing(margin)

class EmptyState(Card):
    def __init__(self, title: str, subtitle: str = "", cta: QPushButton | None = None, parent=None):
        super().__init__(parent)
        self.title = QLabel(title)
        self.title.setStyleSheet("font-weight: 700; font-size: 18px")
        self.subtitle = QLabel(subtitle)
        self.subtitle.setStyleSheet("color: #a7b2c3;")
        self.subtitle.setWordWrap(True)
        self.lay.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.lay.addWidget(self.subtitle, alignment=Qt.AlignmentFlag.AlignHCenter)
        if cta:
            self.lay.addWidget(cta, alignment=Qt.AlignmentFlag.AlignHCenter)

def set_variant(btn: QPushButton, variant: str):
    btn.setProperty("variant", variant)
    btn.style().unpolish(btn); btn.style().polish(btn); btn.update()
