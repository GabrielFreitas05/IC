import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from fpdf import FPDF  

def gerar_relatorio(descricao, data_inicio, data_fim, usuario_id):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Relatório do Teste", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Descrição: {descricao}", ln=True)
    pdf.cell(200, 10, txt=f"Data de Início: {data_inicio}", ln=True)
    pdf.cell(200, 10, txt=f"Data de Fim: {data_fim}", ln=True)
    pdf.cell(200, 10, txt=f"Usuário ID: {usuario_id}", ln=True)

    pdf_file_name = f"relatorio_teste_{descricao}.pdf"
    pdf.output(pdf_file_name)
    messagebox.showinfo("Relatório Gerado", f"Relatório gerado: {pdf_file_name}")

def tela_historico(usuario_id):
    historico_window = tk.Tk()
    historico_window.title("Histórico de Testes")
    historico_window.geometry("600x400")

    # Criação da tabela
    columns = ("descricao", "data_inicio", "data_fim")
    tree = ttk.Treeview(historico_window, columns=columns, show='headings')
    tree.heading("descricao", text="Descrição")
    tree.heading("data_inicio", text="Data de Início")
    tree.heading("data_fim", text="Data de Fim")

    tree.pack(fill=tk.BOTH, expand=True)

    # Carregar dados do banco de dados
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT descricao, data_inicio, data_fim FROM testes WHERE usuario_id = ?', (usuario_id,))
    testes = cursor.fetchall()
    conexao.close()

    if not testes:
        messagebox.showinfo("Histórico", "Nenhum teste encontrado.")
    else:
        for teste in testes:
            tree.insert("", tk.END, values=teste)

    def gerar_relatorio_selecionado():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção Vazia", "Por favor, selecione um teste.")
            return
        descricao, data_inicio, data_fim = tree.item(selected_item, 'values')
        gerar_relatorio(descricao, data_inicio, data_fim, usuario_id)

    
    button_relatorio = tk.Button(historico_window, text="Gerar Relatório", command=gerar_relatorio_selecionado)
    button_relatorio.pack(pady=10)

    tk.Button(historico_window, text="Voltar", command=historico_window.destroy).pack(pady=10)
    

    historico_window.mainloop()
