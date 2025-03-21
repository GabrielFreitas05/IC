import tkinter as tk
from auth import registrar_usuario
from tkinter import messagebox

from telas import tela_usuario

def tela_registro():
    registro_window = tk.Toplevel()
    registro_window.title("Registro")
    registro_window.geometry("1920x1080")

    tk.Label(registro_window, text="E-mail").pack(pady=5)
    email_entry = tk.Entry(registro_window)
    email_entry.pack(pady=5)

    tk.Label(registro_window, text="Senha").pack(pady=5)
    password_entry = tk.Entry(registro_window, show="*")
    password_entry.pack(pady=5)

    tk.Button(registro_window, text="Registrar", command=lambda: registrar(email_entry.get(), password_entry.get(), registro_window)).pack(pady=10)

def registrar(email, password, nome, registro_window):
    if registrar_usuario(email, password, nome):
        messagebox.showinfo("Sucesso", "Registro realizado com sucesso!")
        registro_window.destroy()
        tela_usuario(nome)
