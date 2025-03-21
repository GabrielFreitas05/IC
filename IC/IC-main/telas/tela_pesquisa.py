import tkinter as tk
from tkinter import messagebox, filedialog
from db.db import pesquisar_testes
from pdf_generator.pdf_generator import gerar_pdf
from datetime import datetime

def voltar_tela_inicial(usuario_id):
    pesquisa_window.destroy()
    from telas.tela_usuario import tela_usuario
    tela_usuario(usuario_id)

def tela_pesquisa(usuario_id):
    def realizar_pesquisa():
        material = entry_material.get().strip()
        if not material:
            messagebox.showerror("Erro", "Por favor, insira um material.")
            return
        resultados = pesquisar_testes(material)
        if resultados:
            exibir_resultados(resultados)
        else:
            messagebox.showinfo("Nenhum Resultado", "Nenhum teste encontrado para o material informado.")

    def exibir_resultados(resultados):
        for widget in frame_resultados.winfo_children():
            widget.destroy()
        for idx, resultado in enumerate(resultados):
            titulo = resultado[3]
            data_inicio = resultado[6]
            data_fim = resultado[7]
            autor = resultado[8]
            try:
                data_inicio_formatada = datetime.strptime(data_inicio, "%d-%m-%y").strftime("%d/%m/%y")
                data_fim_formatada = datetime.strptime(data_fim, "%d-%m-%y").strftime("%d/%m/%y")
            except ValueError:
                data_inicio_formatada = data_inicio
                data_fim_formatada = data_fim
            row_frame = tk.Frame(frame_resultados, bg="#333", pady=5)
            row_frame.pack(fill="x", padx=10, pady=2)
            tk.Label(row_frame, text=f"Título: {titulo}", fg="white", bg="#333").pack(side="left", padx=10)
            tk.Label(row_frame, text=f"Data Início: {data_inicio_formatada}", fg="white", bg="#333").pack(side="left", padx=10)
            tk.Label(row_frame, text=f"Data Fim: {data_fim_formatada}", fg="white", bg="#333").pack(side="left", padx=10)
            tk.Label(row_frame, text=f"Autor: {autor}", fg="white", bg="#333").pack(side="left", padx=10)
            button_gerar_pdf = tk.Button(row_frame, text="Gerar Relatório", command=lambda r=resultado: gerar_relatorio_pdf(r), **button_style)
            button_gerar_pdf.pack(side="right", padx=10)
            button_gerar_pdf.bind("<Enter>", lambda e, b=button_gerar_pdf: b.config(bg="#444"))
            button_gerar_pdf.bind("<Leave>", lambda e, b=button_gerar_pdf: b.config(bg="#222"))

    def gerar_relatorio_pdf(resultado):
        caminho = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if caminho:
            titulo = resultado[2]
            descricao = resultado[3]
            data_inicio = resultado[7]
            data_fim = resultado[8]
            
            if caminho != "": 
                gerar_pdf(usuario_id, descricao, "", "", "", "", "", data_inicio, data_fim)
                messagebox.showinfo("Sucesso", f"Relatório para {titulo} gerado com sucesso!")

    pesquisa_window = tk.Tk()
    pesquisa_window.title("Pesquisa de Testes")
    pesquisa_window.geometry("1024x600")
    pesquisa_window.configure(bg="#222")

    button_style = {
        "bg": "#222",
        "fg": "white",
        "activebackground": "#555",
        "activeforeground": "white",
        "bd": 0,
        "padx": 10,
        "pady": 5,
        "relief": "flat",
        "font": ("Arial", 10, "bold"),
        "cursor": "hand2"
    }

    tk.Label(pesquisa_window, text="Pesquisar por Material:", fg="white", bg="#222", font=("Arial", 12)).pack(pady=5)
    entry_material = tk.Entry(pesquisa_window, bg="#333", fg="white", insertbackground="white", font=("Arial", 12), relief="flat")
    entry_material.pack(pady=5, padx=20, ipadx=5, ipady=5, fill="x")

    button_pesquisar = tk.Button(pesquisa_window, text="Pesquisar", command=realizar_pesquisa, **button_style)
    button_pesquisar.pack(pady=10)
    button_pesquisar.bind("<Enter>", lambda e: button_pesquisar.config(bg="#444"))
    button_pesquisar.bind("<Leave>", lambda e: button_pesquisar.config(bg="#222"))

    frame_resultados = tk.Frame(pesquisa_window, bg="#222")
    frame_resultados.pack(pady=10, fill="both", expand=True)

    pesquisa_window.mainloop()
