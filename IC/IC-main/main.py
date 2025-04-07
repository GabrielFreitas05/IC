from PyQt6.QtWidgets import QApplication
import sys
from telas.tela_login import tela_login
from db.db import inicializar_banco 

if __name__ == "__main__":
    inicializar_banco()
    
    app = QApplication(sys.argv)
    tela_login()
    sys.exit(app.exec())
