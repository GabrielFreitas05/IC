import sqlite3

def zerar_banco():
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()


    cursor.execute('DROP TABLE IF EXISTS usuarios')
    cursor.execute('DROP TABLE IF EXISTS testes')


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS testes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        descricao TEXT,
        resultado TEXT,
        equipamentos TEXT,
        om_responsavel TEXT,
        data_inicio TEXT,
        data_fim TEXT,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
    )
    ''')

    conexao.commit()
    conexao.close()
    print("Banco de dados zerado e recriado com sucesso!")

zerar_banco()
