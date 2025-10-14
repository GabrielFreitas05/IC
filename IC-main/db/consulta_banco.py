from db.connection import get_connection


def mostrar_dados():
    conexao = get_connection('usuarios.db')
    cursor = conexao.cursor()
    
    cursor.execute("SELECT * FROM testes")
    dados = cursor.fetchall()
    
    for linha in dados:
        print(linha)
    
    conexao.close()

mostrar_dados()
