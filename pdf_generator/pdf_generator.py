import sqlite3
from tkinter import messagebox
from fpdf import FPDF

def gerar_pdf(usuario_id, descricao, resultado, equipamentos, om_responsavel, data_inicio, data_fim):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Descrição: {descricao}", ln=True)
    pdf.cell(200, 10, txt=f"Resultado: {resultado}", ln=True)
    pdf.cell(200, 10, txt=f"Equipamentos: {equipamentos}", ln=True)
    pdf.cell(200, 10, txt=f"OM Responsável: {om_responsavel}", ln=True)
    pdf.cell(200, 10, txt=f"Data Início: {data_inicio}", ln=True)
    pdf.cell(200, 10, txt=f"Data Fim: {data_fim}", ln=True)

    pdf.output("resultado_teste.pdf")

def salvar_teste(usuario_id, descricao, resultado, equipamentos, om_responsavel, data_inicio, data_fim):
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    try:
        cursor.execute('''
            INSERT INTO testes (usuario_id, descricao, resultado, equipamentos, om_responsavel, data_inicio, data_fim)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (usuario_id, descricao, resultado, equipamentos, om_responsavel, data_inicio, data_fim))
        
        conexao.commit()
        
        gerar_pdf(usuario_id, descricao, resultado, equipamentos, om_responsavel, data_inicio, data_fim)
        messagebox.showinfo("Sucesso", "Teste salvo e PDF gerado com sucesso!")
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao salvar teste: {e}")
    finally:
        conexao.close()

