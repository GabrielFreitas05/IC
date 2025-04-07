import sqlite3
from fpdf import FPDF

def inicializar_banco():
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()

    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            nome TEXT NOT NULL,
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
            historico_revisoes TEXT,
            responsavel TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        ''')

        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
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
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao listar PTA: {e}")
        return []
    finally:
        conexao.close()

def salvar_teste(usuario_id, titulo_procedimento, codigo_documento, versao, data_emissao, objetivo, aplicacao_escopo, responsabilidades, materiais_equipamentos, procedimento_operacional, preparacao, operacao, finalizacao, segurancas_riscos, anexos, historico_revisoes, responsavel):
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()

    try:
        cursor.execute('''
        INSERT INTO testes (usuario_id, titulo_procedimento, codigo_documento, versao, data_emissao, objetivo, aplicacao_escopo, responsabilidades, materiais_equipamentos, procedimento_operacional, preparacao, operacao, finalizacao, segurancas_riscos, anexos, historico_revisoes, responsavel)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (usuario_id, titulo_procedimento, codigo_documento, versao, data_emissao, objetivo, aplicacao_escopo, responsabilidades, materiais_equipamentos, procedimento_operacional, preparacao, operacao, finalizacao, segurancas_riscos, anexos, historico_revisoes, responsavel))

        conexao.commit()
        gerar_pdf(usuario_id, titulo_procedimento, codigo_documento, versao, data_emissao, objetivo, aplicacao_escopo, responsabilidades, materiais_equipamentos, procedimento_operacional, preparacao, operacao, finalizacao, segurancas_riscos, anexos, historico_revisoes)
    except sqlite3.Error as e:
        print(f"Erro ao salvar teste: {e}")
    finally:
        conexao.close()


def gerar_pdf(usuario_id, titulo_procedimento, codigo_documento, versao, data_emissao, objetivo, aplicacao_escopo, responsabilidades, materiais_equipamentos, procedimento_operacional, preparacao, operacao, finalizacao, segurancas_riscos, anexos, historico_revisoes):
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
    pdf.cell(200, 10, txt=f"Histórico de Previsões: {historico_revisoes}", ln=True)

    nome_arquivo = f"{codigo_documento}_{versao}.pdf".replace(" ", "_")
    pdf.output(nome_arquivo)
    print(f"PDF gerado: {nome_arquivo}")

def pesquisar_testes(titulo_procedimento):
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT * FROM testes WHERE titulo_procedimento LIKE ?", ('%' + titulo_procedimento + '%',))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao pesquisar testes: {e}")
        return []
    finally:
        conexao.close()


def pesquisar_pta_por_mes_ano(mes, ano):
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT * FROM pta WHERE strftime('%m', data) = ? AND strftime('%Y', data) = ?", (mes, ano))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao pesquisar PTA por mês e ano: {e}")
        return []
    finally:
        conexao.close()

def listar_testes():
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT * FROM testes")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao listar testes: {e}")
        return []
    finally:
        conexao.close()

