import bcrypt
import sqlite3
from tkinter import messagebox

def gerar_hash_senha(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def verificar_senha(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

def registrar_usuario(email, password):
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
    
    if cursor.fetchone():
        messagebox.showerror("Erro", "Usuário já cadastrado.")
        conexao.close()
        return False

    hashed_password = gerar_hash_senha(password)
    cursor.execute('INSERT INTO usuarios (email, senha) VALUES (?, ?)', (email, hashed_password))
    conexao.commit()
    conexao.close()
    return True  

def login_usuario(email, password):
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
    user = cursor.fetchone()
    conexao.close()
    
    if user:
        stored_password = user[2]
        if verificar_senha(stored_password, password):
            return user[0] 
        else:
            messagebox.showerror("Erro", "Senha incorreta.")
    else:
        messagebox.showerror("Erro", "Usuário não encontrado.")
    return None
