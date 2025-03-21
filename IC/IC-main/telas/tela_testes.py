import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from db.db import salvar_teste

def tela_testes(usuario_id):
    testes_window = tk.Tk()
    testes_window.title("Tela de Testes")
    testes_window.geometry("900x700")
    testes_window.config(bg="#e0e0e0")

    main_frame = tk.Frame(testes_window, bg="#ffffff", bd=2, relief="ridge", padx=20, pady=20)
    main_frame.place(relx=0.5, rely=0.5, anchor="center", width=850, height=650)

    canvas = tk.Canvas(main_frame, bg="#ffffff")
    scroll_y = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scroll_x = tk.Scrollbar(main_frame, orient="horizontal", command=canvas.xview)

    frame = tk.Frame(canvas, bg="#ffffff")
    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)

    def ajustar_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", ajustar_scroll)

    def rolar_com_mouse(event):
        if event.delta > 0:
            canvas.yview_scroll(-1, "units")
        else:
            canvas.yview_scroll(1, "units")
    canvas.bind_all("<MouseWheel>", rolar_com_mouse)


    tk.Label(frame, text="Cadastro de POP (Procedimento Operacional Padrão)", font=("Helvetica", 18, "bold"), bg="#ffffff").grid(row=0, column=0, columnspan=2, pady=10)

    campos = [
        "Título do Procedimento", "Código do Documento", "Versão", "Data de Emissão",
        "Responsável", "Objetivo", "Aplicação e Escopo", "Responsabilidades",
        "Materiais e Equipamentos", "Procedimento Operacional", "Preparação",
        "Operação", "Finalização", "Seguranças e Riscos", "Anexos", "Histórico de Revisões"
    ]

    campos_map = {
        "Título do Procedimento": "titulo_procedimento",
        "Código do Documento": "codigo_documento",
        "Versão": "versao",
        "Data de Emissão": "data_emissao",
        "Responsável": "responsavel",
        "Objetivo": "objetivo",
        "Aplicação e Escopo": "aplicacao_escopo",
        "Responsabilidades": "responsabilidades",
        "Materiais e Equipamentos": "materiais_equipamentos",
        "Procedimento Operacional": "procedimento_operacional",
        "Preparação": "preparacao",
        "Operação": "operacao",
        "Finalização": "finalizacao",
        "Seguranças e Riscos": "segurancas_riscos",
        "Anexos": "anexos",
        "Histórico de Revisões": "historico_previsoes"
    }

    entradas = {}

    for i, campo in enumerate(campos):
        tk.Label(frame, text=campo + ":", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=i + 1, column=0, sticky="w", pady=5)
        if campo in ["Objetivo", "Aplicação e Escopo", "Procedimento Operacional", "Preparação", "Operação", "Finalização", "Seguranças e Riscos", "Anexos", "Histórico de Revisões"]:
            entradas[campo] = tk.Text(frame, font=("Helvetica", 12), height=4, width=60, wrap="word")
            entradas[campo].grid(row=i + 1, column=1, sticky="ew", padx=10, pady=5)
        else:
            entradas[campo] = tk.Entry(frame, font=("Helvetica", 12), width=60)
            entradas[campo].grid(row=i + 1, column=1, sticky="ew", padx=10, pady=5)

    def salvar():
        valores = {
            campos_map[campo]: entradas[campo].get("1.0", tk.END).strip() if isinstance(entradas[campo], tk.Text) else entradas[campo].get().strip()
            for campo in campos
        }
        
        if any(not v for v in valores.values()):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return
        
        salvar_teste(usuario_id, **valores)
        messagebox.showinfo("Sucesso", "Procedimento salvo com sucesso.")

    tk.Button(frame, text="Salvar POP", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", relief="flat", command=salvar).grid(row=len(campos) + 1, column=0, columnspan=2, pady=20)

    testes_window.mainloop()
