import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from fpdf import FPDF
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime



from telas import tela_usuario

def salvar_teste(usuario_id, descricao, resultado, equipamentos, om_responsavel, data_inicio, data_fim):
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    
    try:
        data_inicio_dt = datetime.strptime(data_inicio, '%m/%d/%y').strftime('%Y-%m-%d')
        data_fim_dt = datetime.strptime(data_fim, '%m/%d/%y').strftime('%Y-%m-%d')

        cursor.execute(''' 
        INSERT INTO testes (usuario_id, descricao, resultado, equipamentos, om_responsavel, data_inicio, data_fim)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (usuario_id, descricao, resultado, equipamentos, om_responsavel, data_inicio_dt, data_fim_dt))

        conexao.commit()
        messagebox.showinfo("Sucesso", "Teste salvo com sucesso!")
        gerar_pdf(usuario_id, descricao, resultado, equipamentos, om_responsavel, data_inicio_dt, data_fim_dt)
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao salvar teste: {e}")
    finally:
        conexao.close()

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

def recuperar_testes(usuario_id):
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT descricao, data_inicio, data_fim FROM testes WHERE usuario_id = ?', (usuario_id,))
    testes = cursor.fetchall()

    conexao.close()
    return testes

def exibir_grafico_gantt(usuario_id):
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT descricao, data_inicio, data_fim FROM testes WHERE usuario_id = ?", (usuario_id,))
    dados = cursor.fetchall()

    tarefas = []
    datas_inicio = []
    datas_fim = []

    for descricao, data_inicio, data_fim in dados:
        try:
            data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d')
            data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d')
            tarefas.append(descricao)
            datas_inicio.append(data_inicio_dt)
            datas_fim.append(data_fim_dt)
        except ValueError as e:
            print(f"Erro ao processar datas do teste '{descricao}': {e}")

    fig, ax = plt.subplots()
    bars = []
    for i in range(len(tarefas)):
        bar = ax.barh(tarefas[i], (datas_fim[i] - datas_inicio[i]).days, left=datas_inicio[i].toordinal(), align='center')
        bars.append(bar)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    plt.xlabel('Datas')
    plt.ylabel('Tarefas')
    plt.title('Gráfico de Atividade do usuário: {nome}')

    def on_click(event):
        for bar in bars:
            for rectangle in bar:
                if rectangle.contains(event.x, event.y):
                    descricao = tarefas[bars.index(bar)]
                    messagebox.showinfo("Teste", f"Descrição: {descricao}")

    fig.canvas.mpl_connect('button_press_event', on_click)
    plt.show()
    conexao.close()

def limpar_campos():
    descricao_entry.delete("1.0", tk.END)
    resultado_entry.delete(0, tk.END)
    equipamentos_entry.delete(0, tk.END)
    om_responsavel_entry.delete(0, tk.END)
    data_inicio_entry.set_date(datetime.today())
    data_fim_entry.set_date(datetime.today())

def voltar_tela_inicial(usuario_id):
    testes_window.destroy()  
    tela_usuario(usuario_id)  

def tela_testes(usuario_id):
    global testes_window
    global descricao_entry, resultado_entry, equipamentos_entry, om_responsavel_entry, data_inicio_entry, data_fim_entry

    testes_window = tk.Tk()
    testes_window.title("Tela de Testes")
    testes_window.geometry("800x600")

    tk.Label(testes_window, text="Descrição do Teste:").pack()
    descricao_entry = tk.Text(testes_window, height=5, width=50)
    descricao_entry.pack()

    tk.Label(testes_window, text="Resultado:").pack()
    resultado_entry = tk.Entry(testes_window)
    resultado_entry.pack()

    tk.Label(testes_window, text="Equipamentos:").pack()
    equipamentos_entry = tk.Entry(testes_window)
    equipamentos_entry.pack()

    tk.Label(testes_window, text="OM Responsável:").pack()
    om_responsavel_entry = tk.Entry(testes_window)
    om_responsavel_entry.pack()

    tk.Label(testes_window, text="Data Início:").pack()
    data_inicio_entry = DateEntry(testes_window, width=12, background='darkblue', foreground='white', borderwidth=2)
    data_inicio_entry.pack()

    tk.Label(testes_window, text="Data Fim:").pack()
    data_fim_entry = DateEntry(testes_window, width=12, background='darkblue', foreground='white', borderwidth=2)
    data_fim_entry.pack()

    tk.Button(testes_window, text="Salvar Teste", command=lambda: salvar_teste(
        usuario_id,
        descricao_entry.get("1.0", tk.END).strip(),
        resultado_entry.get(),
        equipamentos_entry.get(),
        om_responsavel_entry.get(),
        data_inicio_entry.get(),
        data_fim_entry.get()
    )).pack(pady=10)

    tk.Button(testes_window, text="Mostrar Gráfico de Gantt", command=lambda: exibir_grafico_gantt(usuario_id)).pack(pady=10)

    tk.Button(testes_window, text="Voltar à Tela Inicial", command=lambda: voltar_tela_inicial(usuario_id)).pack(pady=10)

    tk.Button(testes_window, text="Sair", command=testes_window.destroy).pack(pady=10)

    testes_window.mainloop()

if __name__ == "__main__":
    usuario_id = 1
    tela_testes(usuario_id)
