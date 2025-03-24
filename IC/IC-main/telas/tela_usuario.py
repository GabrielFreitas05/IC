import tkinter as tk
from telas.tela_testes import tela_testes
from telas.tela_pesquisa import tela_pesquisa
from telas.tela_historico import tela_historico
from telas.tela_pta import tela_pta

def tela_usuario(usuario_id):
    def ir_para_pesquisa():
        usuario_window.destroy()
        tela_pesquisa(usuario_id)

    usuario_window = tk.Tk()
    usuario_window.title("Tela Inicial")
    usuario_window.geometry("1920x1080")

    button_testes = tk.Button(usuario_window, text="Procedimento Operacional Padrão (POP)", command=lambda: [usuario_window.destroy(), tela_testes(usuario_id)])
    button_testes.pack()

    button_pta = tk.Button(usuario_window, text="PTA", command=lambda: [usuario_window.destroy(), tela_pta(usuario_id)])
    button_pta.pack()


    button_pesquisa = tk.Button(usuario_window, text="Pesquisar Dados", command=lambda: [usuario_window.destroy(), tela_pesquisa(usuario_id)])
    button_pesquisa.pack()

    button_historico = tk.Button(usuario_window, text="Meu histórico de dados", command=lambda: tela_historico(usuario_id))  
    button_historico.pack(pady=10)
    usuario_window.mainloop()
