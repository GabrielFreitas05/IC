import sqlite3
from tkinter import messagebox, filedialog
from fpdf import FPDF

def gerar_pdf(usuario_id, descricao, resultado, equipamentos, om_responsavel, autor, titulo, data_inicio, data_fim):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Salvar Relatório"
    )
    
    if not file_path:
        messagebox.showwarning("Aviso", "Salvamento cancelado pelo usuário.")
        return
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Descrição: {descricao}", ln=True)
    pdf.cell(200, 10, txt=f"Resultado: {resultado}", ln=True)
    pdf.cell(200, 10, txt=f"Equipamentos: {equipamentos}", ln=True)
    pdf.cell(200, 10, txt=f"OM Responsável: {om_responsavel}", ln=True)
    pdf.cell(200, 10, txt=f"Data Início: {data_inicio}", ln=True)
    pdf.cell(200, 10, txt=f"Data Fim: {data_fim}", ln=True)
    pdf.cell(200, 10, txt=f"Autor: {autor}", ln=True)  
    pdf.cell(200, 10, txt=f"Título: {titulo}", ln=True)
    
    pdf.output(file_path)
    messagebox.showinfo("Sucesso", f"Relatório salvo em: {file_path}")

def salvar_teste(usuario_id, descricao, resultado, equipamentos, om_responsavel, autor, titulo, data_inicio, data_fim):
    conexao = get_connection(
('usuarios.db')
    cursor = conexao.cursor()
    try:
        cursor.execute('''
            INSERT INTO testes (usuario_id, descricao, resultado, equipamentos, om_responsavel, autor, titulo, data_inicio, data_fim)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (usuario_id, descricao, resultado, equipamentos, om_responsavel, autor, titulo, data_inicio, data_fim))
        
        conexao.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao salvar teste: {e}")
    finally:
        conexao.close()
