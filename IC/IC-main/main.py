from db.db import inicializar_banco
from telas.tela_login import tela_login
from db.db import inicializar_banco, salvar_teste


if __name__ == "__main__":
    inicializar_banco()
    tela_login()
