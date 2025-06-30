import sqlite3

def mostrar_dados():
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    
    cursor.execute("SELECT * FROM testes")
    dados = cursor.fetchall()
    
    for linha in dados:
        print(linha)
    
    conexao.close()

mostrar_dados()
