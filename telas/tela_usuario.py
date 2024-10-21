from os import name
import tkinter as tk
from telas.tela_testes import tela_testes

def tela_usuario(usuario_id):
    usuario_window = tk.Tk()
    usuario_window.title("Tela do Usuário")
    usuario_window.geometry("800x600")

    button_testes = tk.Button(usuario_window, text="Ir para Testes", command=lambda: [usuario_window.destroy(), tela_testes(usuario_id)])
    button_testes.pack()
    
    usuario_window.mainloop()

   

