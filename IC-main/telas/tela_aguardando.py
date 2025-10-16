from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QTimer

class TelaAguardando(QDialog):
    def __init__(self, email, check_fn, open_login_fn):
        super().__init__()
        self.email = email
        self.check_fn = check_fn
        self.open_login_fn = open_login_fn
        self.setWindowTitle("Aguardando aprovação")
        self.setFixedSize(380, 220)
        layout = QVBoxLayout(self)
        self.lbl = QLabel(f"Seu cadastro {email} aguarda aprovação do administrador.")
        self.lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_login = QPushButton("Voltar ao login")
        self.btn_sair = QPushButton("Sair")
        layout.addWidget(self.lbl)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_sair)
        self.btn_login.clicked.connect(self.voltar_login)
        self.btn_sair.clicked.connect(self.close)
        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.verificar)
        self.timer.start()

    def verificar(self):
        try:
            aprovado = self.check_fn(self.email)
            if aprovado:
                self.timer.stop()
                self.lbl.setText("Aprovado. Volte ao login para acessar.")
                self.btn_login.setFocus()
        except Exception:
            pass

    def voltar_login(self):
        self.close()
        self.open_login_fn()
