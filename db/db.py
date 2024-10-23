import sqlite3
from datetime import datetime

def inicializar_banco():
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
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



def obter_historico_testes():
    conn = sqlite3.connect('usuarios.db') 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM testes")  
    resultados = cursor.fetchall()
    conn.close()
    return resultados




def atualizar_dados_existentes():
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()

    cursor.execute("SELECT id, data_inicio, data_fim FROM testes")
    testes = cursor.fetchall()

    for teste in testes:
        teste_id = teste[0]
        data_inicio_str = teste[1]
        data_fim_str = teste[2]

        print(f"Teste ID: {teste_id}, Data Início: {data_inicio_str}, Data Fim: {data_fim_str}")

        try:
            if data_inicio_str:
                data_inicio_dt = datetime.strptime(data_inicio_str, '%Y-%m-%d').strftime('%Y-%m-%d')
            else:
                data_inicio_dt = None

            if data_fim_str:
                data_fim_dt = datetime.strptime(data_fim_str, '%Y-%m-%d').strftime('%Y-%m-%d')
            else:
                data_fim_dt = None

            cursor.execute("UPDATE testes SET data_inicio = ?, data_fim = ? WHERE id = ?", 
                           (data_inicio_dt, data_fim_dt, teste_id))
            print(f"Atualizado teste ID {teste_id}: {data_inicio_str} -> {data_inicio_dt}, {data_fim_str} -> {data_fim_dt}")
        except ValueError as ve:
            print(f"Erro ao processar teste ID {teste_id}: {ve}")

    conexao.commit()
    conexao.close()
