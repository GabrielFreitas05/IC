# ui/theme.py
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

TOKENS = {
    "radius": 12,
    "space": 12,
    "font_family": "Segoe UI, Arial, Helvetica, sans-serif",
    "font_size": 14,
    # Dark palette
    "dark": {
        "bg": "#0b1220",
        "surface": "#0f172a",
        "surface-soft": "#111827",
        "border": "#1e293b",
        "text": "#e2e8f0",
        "text-muted": "#a7b2c3",
        "accent": "#FFCD00",
        "accent-hover": "#e6b800",
        "danger": "#ef4444",
        "ok": "#22c55e",
        "info": "#3b82f6",
    },
    # Light palette (opcional)
    "light": {
        "bg": "#f7f8fb",
        "surface": "#ffffff",
        "surface-soft": "#f1f5f9",
        "border": "#d0d7e2",
        "text": "#0f172a",
        "text-muted": "#445065",
        "accent": "#FFCD00",
        "accent-hover": "#e6b800",
        "danger": "#e11d48",
        "ok": "#16a34a",
        "info": "#2563eb",
    },
}

def build_stylesheet(mode: str = "dark") -> str:
    t = TOKENS[mode]
    r = TOKENS["radius"]
    b = t["border"]
    return f"""
    /* Base */
    * {{
        font-family: {TOKENS["font_family"]};
        font-size: {TOKENS["font_size"]}px;
    }}
    QMainWindow, QDialog, QWidget {{
        background-color: {t["bg"]};
        color: {t["text"]};
    }}
    QLabel#title {{
        color: {t["accent"]};
        font-size: 22px;
        font-weight: 700;
        letter-spacing: .5px;
    }}
    /* Cards */
    .Card {{
        background: {t["surface"]};
        border: 1px solid {b};
        border-radius: {r}px;
    }}
    /* Buttons */
    QPushButton {{
        background-color: {t["accent"]};
        color: {TOKENS["dark"]["bg"] if mode=="light" else "#0f172a"};
        border: 0;
        padding: 10px 16px;
        border-radius: {r-2}px;
        font-weight: 600;
    }}
    QPushButton:hover {{ background-color: {t["accent-hover"]}; }}
    QPushButton:disabled {{ background: #586273; color: #b5bfcd; }}
    QPushButton[variant="secondary"] {{
        background: {t["surface-soft"]};
        color: {t["text"]};
        border: 1px solid {b};
    }}
    QPushButton[variant="secondary"]:hover {{ background: {"#e8eef7" if mode=="light" else "#162235"}; }}
    QPushButton[variant="danger"] {{ background: {t["danger"]}; color: white; }}
    QPushButton[variant="danger"]:hover {{ background: {"#be123c" if mode=="light" else "#dc2626"}; }}

    /* Inputs */
    QLineEdit, QTextEdit, QDateEdit, QComboBox, QSpinBox {{
        background: {t["surface"]};
        border: 1px solid {b};
        padding: 8px 10px;
        border-radius: {r-2}px;
        selection-background-color: {t["accent"]};
        selection-color: {"#0f172a" if mode=="dark" else "#0f172a"};
    }}
    QComboBox QAbstractItemView {{
        background: {t["surface"]};
        color: {t["text"]};
        border: 1px solid {b};
        selection-background-color: {t["accent"]};
        selection-color: #0f172a;
    }}

    /* Tabs */
    QTabWidget::pane {{
        border: 1px solid {b};
        background: {t["surface"]};
        border-radius: {r}px;
        top: -1px;
    }}
    QTabBar::tab {{
        background: {t["surface-soft"]};
        color: {t["text"]};
        padding: 8px 18px;
        border: 1px solid {b};
        border-bottom: none;
        border-top-left-radius: {r-2}px;
        border-top-right-radius: {r-2}px;
        margin-right: 6px;
    }}
    QTabBar::tab:hover {{ background: {"#e8eef7" if mode=="light" else "#1a2942"}; }}
    QTabBar::tab:selected {{
        background: {t["accent"]};
        color: #0f172a;
        border-color: {t["accent"]};
    }}
    QTabBar::tab:!selected {{ margin-top: 4px; }}

    /* Tables */
    QTableWidget {{
        background: {t["surface"]};
        gridline-color: {b};
        border: 1px solid {b};
        border-radius: {r}px;
        alternate-background-color: {"#f7f9fc" if mode=="light" else "#0c1526"};
    }}
    QHeaderView::section {{
        background: {t["surface-soft"]};
        color: {t["text"]};
        padding: 10px 8px;
        border: none;
        font-weight: 600;
        border-right: 1px solid {b};
    }}
    QTableWidget::item:selected {{
        background: {t["accent"]};
        color: #0f172a;
    }}

    /* Scrollbars */
    QScrollBar:vertical {{
        background: transparent; width: 12px; margin: 12px 0 12px 0;
    }}
    QScrollBar::handle:vertical {{
        background: {"#d4dae6" if mode=="light" else "#263246"}; min-height: 32px; border-radius: 6px;
    }}
    QScrollBar::handle:vertical:hover {{ background: {"#c6cfdf" if mode=="light" else "#2d3a50"}; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}

    QScrollBar:horizontal {{
        background: transparent; height: 12px; margin: 0 12px;
    }}
    QScrollBar::handle:horizontal {{
        background: {"#d4dae6" if mode=="light" else "#263246"}; min-width: 32px; border-radius: 6px;
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}

    /* Focus visível (acessibilidade) */
    *:focus {{
        outline: 2px solid {t["info"]};
        outline-offset: 0px;
    }}
    """

def apply_theme(app: QApplication, mode: str = "dark"):
    # tipografia global (opcional)
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(build_stylesheet(mode))

def toggle_theme(app: QApplication):
    # alterna entre dark e light (se quiser um atalho no app)
    current = app.styleSheet()
    app.setStyleSheet(build_stylesheet("light") if "#0b1220" in current else build_stylesheet("dark"))
