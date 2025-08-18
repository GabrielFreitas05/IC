import sqlite3

def salvar_pta(usuario_id, data, descricao):
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()

    try:
        cursor.execute(''' 
        INSERT INTO pta (usuario_id, data, descricao)
        VALUES (?, ?, ?)
        ''', (usuario_id, data, descricao))

        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao salvar PTA: {e}")
    finally:
        conexao.close()

def inicializar_tabela_pta():
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    
    try:
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS pta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            data TEXT,
            descricao TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        ''')
        
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inicializar a tabela PTA: {e}")
    finally:
        conexao.close()
