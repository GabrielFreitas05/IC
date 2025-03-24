import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from db.pta import salvar_pta
from pdf_generator.pdf_generator import gerar_pdf  # Importando a função para gerar PDF

def tela_pta(usuario_id):
    pta_window = tk.Tk()
    pta_window.title("Envio de PTA")
    pta_window.geometry("1920x1080")
    pta_window.config(bg="#e0e0e0")

    main_frame = tk.Frame(pta_window, bg="#ffffff", bd=2, relief="ridge", padx=20, pady=20)
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

    tk.Label(frame, text="Cadastro de PTA (Procedimento Técnico Administrativo)", font=("Helvetica", 18, "bold"), bg="#ffffff").grid(row=0, column=0, columnspan=2, pady=10)

    campos = [
        "Data", "Descrição"
    ]

    entradas = {}

    for i, campo in enumerate(campos):
        tk.Label(frame, text=campo + ":", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=i + 1, column=0, sticky="w", pady=5)
        if campo == "Data":
            entradas[campo] = DateEntry(frame, font=("Helvetica", 12), width=60, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
            entradas[campo].grid(row=i + 1, column=1, sticky="ew", padx=10, pady=5)
        elif campo == "Descrição":
            entradas[campo] = tk.Text(frame, font=("Helvetica", 12), height=4, width=60, wrap="word")
            entradas[campo].grid(row=i + 1, column=1, sticky="ew", padx=10, pady=5)

    def salvar():
        valores = {
            "data": entradas["Data"].get(),
            "descricao": entradas["Descrição"].get("1.0", tk.END).strip()
        }

        if any(not v for v in valores.values()):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        salvar_pta(usuario_id, valores["data"], valores["descricao"])

        # Perguntar se o usuário quer salvar o relatório
        resposta = messagebox.askyesno("Salvar Relatório", "Deseja salvar em um relatório?")

        if resposta:  # Se o usuário escolher 'Sim', gera o relatório em PDF
            gerar_pdf(usuario_id, valores["descricao"], "", "", "", "", "", valores["data"], valores["data"])  # Ajuste conforme necessário para os parâmetros do PDF.

        messagebox.showinfo("Sucesso", "PTA salvo com sucesso.")

    tk.Button(frame, text="Salvar PTA", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", relief="flat", command=salvar).grid(row=len(campos) + 1, column=0, columnspan=2, pady=20)

    def voltar_para_tela_inicial():
        from telas.tela_usuario import tela_usuario
        tela_usuario(usuario_id)

    tk.Button(frame, text="Voltar para Tela Inicial", font=("Helvetica", 12, "bold"), bg="#FF5733", fg="white", relief="flat", command=voltar_para_tela_inicial).grid(row=len(campos) + 2, column=0, columnspan=2, pady=10)

    pta_window.mainloop()
