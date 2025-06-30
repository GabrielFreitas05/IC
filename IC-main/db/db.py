import sqlite3
from fpdf import FPDF

def conectar():
    return sqlite3.connect('usuarios.db')

def inicializar_banco():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL,
            id_personalizada TEXT NOT NULL UNIQUE
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
            controle_qualidade TEXT,
            manutencao_calibracao TEXT,
            referencias TEXT,
            anexos TEXT,
            historico_revisoes TEXT,
            responsavel TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS processos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            padrao INTEGER DEFAULT 0
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS etapas_processo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            processo_id INTEGER,
            ordem INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            instrucoes TEXT,
            validacao TEXT,
            FOREIGN KEY (processo_id) REFERENCES processos (id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS processo_execucao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            processo_id INTEGER,
            etapa_atual INTEGER,
            data_inicio TEXT,
            data_final TEXT,
            status TEXT,
            dados TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
            FOREIGN KEY (processo_id) REFERENCES processos (id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS formularios_processos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        nome_processo TEXT,
        responsavel TEXT,
        data_inicio TEXT,
        nome_fase TEXT,
        ordem_fase TEXT,
        objetivo_fase TEXT,
        nome_passo TEXT,
        ordem_passo TEXT,
        descricao_passo TEXT,
        ferramentas TEXT,
        tempo_estimado TEXT,
        riscos TEXT,
        entradas TEXT,
        saidas TEXT,
        depende TEXT,
        depende_qual TEXT,
        decisao TEXT,
        fluxo_decisao TEXT,
        tempo_real TEXT,
        qualidade TEXT,
        licoes TEXT,
        melhorias TEXT,
        data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        ''')


        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        conexao.close()

def gerar_id_usuario(nome_usuario):
    partes_nome = nome_usuario.split()
    iniciais = "".join([parte[0].upper() for parte in partes_nome[:2]])
    
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    contador = cursor.fetchone()[0] + 1
    
    id_usuario = f"{iniciais}-{contador:03d}"
    
    conexao.close()
    
    return id_usuario

def salvar_usuario(email, nome, senha):
    id_personalizada = gerar_id_usuario(nome)
    
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute('''
        INSERT INTO usuarios (email, nome, senha, id_personalizada)
        VALUES (?, ?, ?, ?)
        ''', (email, nome, senha, id_personalizada))

        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao salvar usuário: {e}")
    finally:
        conexao.close()

def salvar_pta_db(usuario_id, data, descricao):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute('''
        INSERT INTO pta (usuario_id, data, descricao)
        VALUES (?, ?, ?)
        ''', (usuario_id, data, descricao))

        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao salvar PTA: {e}")
        return False
    finally:
        conexao.close()

def listar_ptas_por_usuario_db(usuario_id):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT * FROM pta WHERE usuario_id = ?", (usuario_id,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao listar PTAs: {e}")
        return []
    finally:
        conexao.close()

def atualizar_pta_db(pta_id, data, descricao):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute('''
        UPDATE pta SET data = ?, descricao = ? WHERE id = ?
        ''', (data, descricao, pta_id))

        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao atualizar PTA: {e}")
        return False
    finally:
        conexao.close()

def listar_pta():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT * FROM pta")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao listar PTA: {e}")
        return []
    finally:
        conexao.close()

def excluir_pta_db(pta_id):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("DELETE FROM pta WHERE id = ?", (pta_id,))
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao excluir PTA: {e}")
        return False
    finally:
        conexao.close()

def gerar_pdf(usuario_id, titulo_procedimento, codigo_documento, versao, data_emissao, objetivo, aplicacao_escopo, responsabilidades, materiais_equipamentos, procedimento_operacional, preparacao, operacao, finalizacao, segurancas_riscos, controle_qualidade, manutencao_calibracao, referencias, anexos, historico_revisoes, responsavel):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Relatório de Teste", ln=True, align='C')
    pdf.ln(10)

    dados = {
        "Título do Procedimento": titulo_procedimento,
        "Código do Documento": codigo_documento,
        "Versão": versao,
        "Data de Emissão": data_emissao,
        "Objetivo": objetivo,
        "Aplicação e Escopo": aplicacao_escopo,
        "Responsabilidades": responsabilidades,
        "Materiais e Equipamentos": materiais_equipamentos,
        "Procedimento Operacional": procedimento_operacional,
        "Preparação": preparacao,
        "Operação": operacao,
        "Finalização": finalizacao,
        "Seguranças e Riscos": segurancas_riscos,
        "Controle de Qualidade": controle_qualidade,
        "Manutenção e Calibração": manutencao_calibracao,
        "Referências": referencias,
        "Anexos": anexos,
        "Histórico de Revisões": historico_revisoes,
        "Responsável": responsavel
    }

    for campo, valor in dados.items():
        pdf.multi_cell(0, 10, txt=f"{campo}: {valor}", align='L')

    nome_arquivo = f"{codigo_documento}_{versao}.pdf".replace(" ", "_")
    pdf.output(nome_arquivo)
    print(f"PDF gerado: {nome_arquivo}")

def pesquisar_testes(titulo_procedimento):
    conexao = conectar()
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
    conexao = conectar()
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
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT * FROM testes")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao listar testes: {e}")
        return []
    finally:
        conexao.close()

def buscar_nome_usuario(usuario_id):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT nome FROM usuarios WHERE id = ?", (usuario_id,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else "Usuário"
    except sqlite3.Error as e:
        print(f"Erro ao buscar nome do usuário: {e}")
        return "Usuário"
    finally:
        conexao.close()

def salvar_teste(usuario_id, **valores):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO testes (
                titulo_procedimento,
                codigo_documento,
                versao,
                data_emissao,
                objetivo,
                aplicacao_escopo,
                responsabilidades,
                materiais_equipamentos,
                procedimento_operacional,
                preparacao,
                operacao,
                finalizacao,
                segurancas_riscos,
                controle_qualidade,
                manutencao_calibracao,
                referencias,
                anexos,
                historico_revisoes,
                responsavel,
                usuario_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            valores.get("titulo_procedimento", ""),
            valores.get("codigo_documento", ""),
            valores.get("versao", ""),
            valores.get("data_emissao", ""),
            valores.get("objetivo", ""),
            valores.get("aplicacao_escopo", ""),
            valores.get("responsabilidades", ""),
            valores.get("materiais_equipamentos", ""),
            valores.get("procedimento_operacional", ""),
            valores.get("preparacao", ""),
            valores.get("operacao", ""),
            valores.get("finalizacao", ""),
            valores.get("segurancas_riscos", ""),
            valores.get("controle_qualidade", ""),
            valores.get("manutencao_calibracao", ""),
            valores.get("referencias", ""),
            valores.get("anexos", ""),
            valores.get("historico_revisoes", ""),
            valores.get("responsavel", ""),
            usuario_id
        ))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao salvar teste: {e}")
    finally:
        conexao.close()

def listar_usuarios():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT * FROM usuarios")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao listar usuários: {e}")
        return []
    finally:
        conexao.close()

def excluir_usuario(usuario_id):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao excluir usuário: {e}")
    finally:
        conexao.close()

def excluir_teste(teste_id):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("DELETE FROM testes WHERE id = ?", (teste_id,))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao excluir teste: {e}")
    finally:
        conexao.close()

def listar_historico_revisoes(teste_id):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT historico_revisoes FROM testes WHERE id = ?", (teste_id,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except sqlite3.Error as e:
        print(f"Erro ao listar histórico de revisões: {e}")
        return None
    finally:
        conexao.close()

def buscar_testes_por_responsavel(responsavel):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT * FROM testes WHERE responsavel LIKE ?", ('%' + responsavel + '%',))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao buscar testes por responsável: {e}")
        return []
    finally:
        conexao.close()

def buscar_id_usuario(id_personalizada):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT id FROM usuarios WHERE id_personalizada = ?", (id_personalizada,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except sqlite3.Error as e:
        print(f"Erro ao buscar ID do usuário: {e}")
        return None
    finally:
        conexao.close()

def salvar_formulario_processo(
    usuario_id,
    nome_processo,
    responsavel,
    data_inicio,
    nome_fase,
    ordem_fase,
    objetivo_fase,
    nome_passo,
    ordem_passo,
    descricao_passo,
    ferramentas,
    tempo_estimado,
    riscos,
    entradas,
    saidas,
    depende,
    depende_qual,
    decisao,
    fluxo_decisao,
    tempo_real,
    qualidade,
    licoes,
    melhorias
):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO formularios_processos (
                usuario_id,
                nome_processo,
                responsavel,
                data_inicio,
                nome_fase,
                ordem_fase,
                objetivo_fase,
                nome_passo,
                ordem_passo,
                descricao_passo,
                ferramentas,
                tempo_estimado,
                riscos,
                entradas,
                saidas,
                depende,
                depende_qual,
                decisao,
                fluxo_decisao,
                tempo_real,
                qualidade,
                licoes,
                melhorias
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            usuario_id,
            nome_processo,
            responsavel,
            data_inicio,
            nome_fase,
            ordem_fase,
            objetivo_fase,
            nome_passo,
            ordem_passo,
            descricao_passo,
            ferramentas,
            tempo_estimado,
            riscos,
            entradas,
            saidas,
            depende,
            depende_qual,
            decisao,
            fluxo_decisao,
            tempo_real,
            qualidade,
            licoes,
            melhorias
        ))
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao salvar formulário: {e}")
        return False
    finally:
        conexao.close()

