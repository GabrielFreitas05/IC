import sqlite3

def visualizar_dados():
    conexao = sqlite3.connect("db/usuarios.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM testes")
    dados = cursor.fetchall()

    for linha in dados:
        print(linha)

    conexao.close()

visualizar_dados()
