import sqlite3
from datetime import datetime
from fpdf import FPDF

def inicializar_banco():
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    
    try:
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
        ''')

        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS pta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            data TEXT,
            descricao TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        ''')

        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS testes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            titulo_procedimento TEXT,
            codigo_documento TEXT,
            versao TEXT,
            data_emissao TEXT,
            objetivo TEXT,
            aplicacao_escopo TEXT,
            responsabilidades TEXT,
            materiais_equipamentos TEXT,
            procedimento_operacional TEXT,
            preparacao TEXT,
            operacao TEXT,
            finalizacao TEXT,
            segurancas_riscos TEXT,
            anexos TEXT,
            historico_previsoes TEXT,
            responsavel TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        ''')

        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        conexao.close()

def excluir_e_recriar_tabela_pta():
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    
    try:
        cursor.execute("DROP TABLE IF EXISTS pta")
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS pta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            data TEXT,
            descricao TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        ''')
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao excluir e recriar a tabela de PTA: {e}")
    finally:
        conexao.close()

def salvar_pta(usuario_id, data, descricao):
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()

    try:
        cursor.execute(''' 
        INSERT INTO pta (usuario_id, data, descricao)
        VALUES (?, ?, ?)
        ''', (usuario_id, data, descricao))

        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao salvar PTA: {e}")
    finally:
        conexao.close()

def listar_pta():
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    
    try:
        cursor.execute("SELECT * FROM pta")
        resultados = cursor.fetchall()
        return resultados
    except sqlite3.Error as e:
        print(f"Erro ao listar PTA: {e}")
        return []
    finally:
        conexao.close()

def excluir_e_recriar_tabela_teste():
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    
    try:
        cursor.execute("DROP TABLE IF EXISTS testes")
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS testes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            titulo_procedimento TEXT,
            codigo_documento TEXT,
            versao TEXT,
            data_emissao TEXT,
            objetivo TEXT,
            aplicacao_escopo TEXT,
            responsabilidades TEXT,
            materiais_equipamentos TEXT,
            procedimento_operacional TEXT,
            preparacao TEXT,
            operacao TEXT,
            finalizacao TEXT,
            segurancas_riscos TEXT,
            anexos TEXT,
            historico_previsoes TEXT,
            responsavel TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        ''')
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao excluir e recriar a tabela de testes: {e}")
    finally:
        conexao.close()

def salvar_teste(usuario_id, titulo_procedimento, codigo_documento, versao, data_emissao, objetivo, aplicacao_escopo, responsabilidades, materiais_equipamentos, procedimento_operacional, preparacao, operacao, finalizacao, segurancas_riscos, anexos, historico_previsoes, responsavel):
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    
    try:
        cursor.execute(''' 
        INSERT INTO testes (usuario_id, titulo_procedimento, codigo_documento, versao, data_emissao, objetivo, aplicacao_escopo, responsabilidades, materiais_equipamentos, procedimento_operacional, preparacao, operacao, finalizacao, segurancas_riscos, anexos, historico_previsoes, responsavel)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (usuario_id, titulo_procedimento, codigo_documento, versao, data_emissao, objetivo, aplicacao_escopo, responsabilidades, materiais_equipamentos, procedimento_operacional, preparacao, operacao, finalizacao, segurancas_riscos, anexos, historico_previsoes, responsavel))
        
        conexao.commit()
        gerar_pdf(usuario_id, titulo_procedimento, codigo_documento, versao, data_emissao, objetivo, aplicacao_escopo, responsabilidades, materiais_equipamentos, procedimento_operacional, preparacao, operacao, finalizacao, segurancas_riscos, anexos, historico_previsoes)
    except sqlite3.Error as e:
        print(f"Erro ao salvar teste: {e}")
    finally:
        conexao.close()

def pesquisar_testes(titulo_procedimento):
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    
    try:
        query = "SELECT * FROM testes WHERE titulo_procedimento LIKE ?"
        cursor.execute(query, ('%' + titulo_procedimento + '%',))
        resultados = cursor.fetchall()
        return resultados
    except sqlite3.Error as e:
        print(f"Erro ao pesquisar testes: {e}")
        return []
    finally:
        conexao.close()

def gerar_pdf(usuario_id, titulo_procedimento, codigo_documento, versao, data_emissao, objetivo, aplicacao_escopo, responsabilidades, materiais_equipamentos, procedimento_operacional, preparacao, operacao, finalizacao, segurancas_riscos, anexos, historico_previsoes):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Relatório de Teste", ln=True, align='C')
    pdf.ln(10)  
    
    pdf.cell(200, 10, txt=f"Título do Procedimento: {titulo_procedimento}", ln=True)
    pdf.cell(200, 10, txt=f"Código do Documento: {codigo_documento}", ln=True)
    pdf.cell(200, 10, txt=f"Versão: {versao}", ln=True)
    pdf.cell(200, 10, txt=f"Data de Emissão: {data_emissao}", ln=True)
    pdf.cell(200, 10, txt=f"Objetivo: {objetivo}", ln=True)
    pdf.cell(200, 10, txt=f"Aplicação e Escopo: {aplicacao_escopo}", ln=True)
    pdf.cell(200, 10, txt=f"Responsabilidades: {responsabilidades}", ln=True)
    pdf.cell(200, 10, txt=f"Materiais e Equipamentos: {materiais_equipamentos}", ln=True)
    pdf.cell(200, 10, txt=f"Procedimento Operacional: {procedimento_operacional}", ln=True)
    pdf.cell(200, 10, txt=f"Preparação: {preparacao}", ln=True)
    pdf.cell(200, 10, txt=f"Operação: {operacao}", ln=True)
    pdf.cell(200, 10, txt=f"Finalização: {finalizacao}", ln=True)
    pdf.cell(200, 10, txt=f"Seguranças e Riscos: {segurancas_riscos}", ln=True)
    pdf.cell(200, 10, txt=f"Anexos: {anexos}", ln=True)
    pdf.cell(200, 10, txt=f"Histórico de Previsões: {historico_previsoes}", ln=True)
    
    nome_arquivo = f"{codigo_documento}_{versao}.pdf".replace(" ", "_")
    pdf.output(nome_arquivo)
    print(f"PDF gerado: {nome_arquivo}")

def listar_testes():
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    
    try:
        cursor.execute("SELECT * FROM testes")
        resultados = cursor.fetchall()
        return resultados
    except sqlite3.Error as e:
        print(f"Erro ao listar testes: {e}")
        return []
    finally:
        conexao.close()
