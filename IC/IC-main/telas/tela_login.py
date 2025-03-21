import tkinter as tk
from tkinter import messagebox
from db.auth import registrar_usuario, login_usuario
from telas.tela_usuario import tela_usuario

def tela_login():
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("1920x1080")

    tk.Label(login_window, text="E-mail").pack(pady=5)
    email_entry = tk.Entry(login_window)
    email_entry.pack(pady=5)

    tk.Label(login_window, text="Senha").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Login", command=lambda: login_and_open(email_entry.get(), password_entry.get(), login_window), bg="blue", fg="white").pack(pady=10)
    tk.Button(login_window, text="Registrar", command=lambda: registrar(email_entry.get(), password_entry.get(), login_window), bg="green", fg="white").pack(pady=10)

    login_window.mainloop()

def login_and_open(email, password, login_window):
    usuario_id = login_usuario(email, password)

    if usuario_id: 
        messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
        login_window.destroy() 
        tela_usuario(usuario_id) 

def registrar(email, password, login_window):
    if email and password:
        if registrar_usuario(email, password): 
            messagebox.showinfo("Sucesso", "Registro realizado com sucesso!")
            login_window.destroy()
            usuario_id = login_usuario(email, password)
            tela_usuario(usuario_id)
        else:
            messagebox.showerror("Erro", "Esse e-mail já está registrado.")
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
