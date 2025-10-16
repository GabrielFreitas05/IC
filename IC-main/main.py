import sys
from PyQt6.QtWidgets import QApplication
from db.db import inicializar_banco
from telas.tela_login import tela_login

try:
    from ui.theme import apply_theme
except Exception:
    apply_theme = None 

if __name__ == "__main__":
    inicializar_banco()

    app = QApplication(sys.argv)
    if apply_theme:
        apply_theme(app, mode="dark")
    tela_login()
    sys.exit(app.exec())
