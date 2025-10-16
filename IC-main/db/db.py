import sqlite3
from fpdf import FPDF
from db.connection import get_connection

def conectar():
    return get_connection('usuarios.db')

def inicializar_banco():
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL,
            id_personalizada TEXT,
            role TEXT NOT NULL DEFAULT 'user',
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS registration_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL,
            id_personalizada TEXT,
            requested_role TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS formularios_processos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            nome_processo TEXT NOT NULL,
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
            status TEXT DEFAULT 'rascunho',
            data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        ''')

        # Garantir a tabela de processos (usada por salvar_processo/listar_processos)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS processos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            padrao INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # Tabela de atividades/timeline do processo (para o "Detalhe")
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS process_activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            process_id INTEGER NOT NULL,
            entry_date TEXT NOT NULL,
            title TEXT NOT NULL,
            note TEXT,
            author_id INTEGER,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (process_id) REFERENCES processos(id) ON DELETE CASCADE
        )
        ''')

        cols = [r[1] for r in cursor.execute("PRAGMA table_info(usuarios)").fetchall()]
        if "id_personalizada" not in cols:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN id_personalizada TEXT")
        if "role" not in cols:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN role TEXT NOT NULL DEFAULT 'user'")
        if "is_active" not in cols:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN is_active INTEGER NOT NULL DEFAULT 1")

        conexao.commit()
    finally:
        conexao.close()

def criar_pedido_cadastro(email, nome, senha_hash, id_personalizada, requested_role):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO registration_requests (email, nome, senha, id_personalizada, requested_role) VALUES (?, ?, ?, ?, ?)",
            (email, nome, senha_hash, id_personalizada, requested_role)
        )
        conexao.commit()
        return cursor.lastrowid
    finally:
        conexao.close()

def listar_pedidos_pendentes():
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT id, email, nome, id_personalizada, requested_role, created_at
            FROM registration_requests
            WHERE status='pending'
            ORDER BY created_at ASC
        """)
        return cursor.fetchall()
    finally:
        conexao.close()

def aprovar_pedido(pedido_id, role_final=None, email_override=None, nome_override=None, idp_override=None):
    conexao = conectar()
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    try:
        row = cursor.execute(
            "SELECT email, nome, senha, id_personalizada, requested_role FROM registration_requests WHERE id=? AND status='pending'",
            (pedido_id,)
        ).fetchone()
        if not row:
            return False
        email = email_override or row["email"]
        nome = nome_override or row["nome"]
        senha = row["senha"]
        idp = idp_override or row["id_personalizada"]
        role = role_final or row["requested_role"]
        cursor.execute(
            "INSERT INTO usuarios (email, nome, senha, id_personalizada, role, is_active) VALUES (?, ?, ?, ?, ?, 1)",
            (email, nome, senha, idp, role)
        )
        cursor.execute("UPDATE registration_requests SET status='approved' WHERE id=?", (pedido_id,))
        conexao.commit()
        return True
    finally:
        conexao.close()

def rejeitar_pedido(pedido_id):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("UPDATE registration_requests SET status='rejected' WHERE id=? AND status='pending'", (pedido_id,))
        conexao.commit()
        return cursor.rowcount > 0
    finally:
        conexao.close()

def gerar_id_usuario(nome_usuario):
    partes_nome = nome_usuario.split()
    iniciais = "".join([parte[0].upper() for parte in partes_nome[:2]]) if partes_nome else "US"
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    contador = cursor.fetchone()[0] + 1
    conexao.close()
    return f"{iniciais}-{contador:03d}"

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
    melhorias,
    status='rascunho'
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
                melhorias,
                status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            melhorias,
            status
        ))
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao salvar formulário: {e}")
        return False
    finally:
        conexao.close()

def salvar_processo(nome, descricao=None, padrao=0):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO processos (nome, descricao, padrao, created_at) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
            (nome, descricao, padrao)
        )
        conexao.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Erro ao salvar processo: {e}")
        return None
    finally:
        conexao.close()

def listar_processos():
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("UPDATE processos SET created_at = COALESCE(created_at, CURRENT_TIMESTAMP) WHERE created_at IS NULL")
        conexao.commit()
        cursor.execute("SELECT id, nome, descricao, padrao, created_at FROM processos ORDER BY id DESC")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao listar processos: {e}")
        return []
    finally:
        conexao.close()

# --------- NOVO: suporte ao Detalhe do Processo (timeline/atividades) ---------

def get_process_header(process_id: int):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id, nome, descricao, padrao, created_at FROM processos WHERE id=?", (process_id,))
        return cursor.fetchone()
    finally:
        conexao.close()

def list_process_activities(process_id: int):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT id, entry_date, title, note, author_id, created_at, updated_at
            FROM process_activities
            WHERE process_id=?
            ORDER BY datetime(entry_date) DESC, id DESC
        """, (process_id,))
        return cursor.fetchall()
    finally:
        conexao.close()

def add_process_activity(process_id: int, entry_date: str, title: str, note: str, author_id: int | None = None):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO process_activities (process_id, entry_date, title, note, author_id)
            VALUES (?, ?, ?, ?, ?)
        """, (process_id, entry_date, title, note, author_id))
        conexao.commit()
        return cursor.lastrowid
    finally:
        conexao.close()

def update_process_activity(activity_id: int, entry_date: str, title: str, note: str):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            UPDATE process_activities
            SET entry_date=?, title=?, note=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        """, (entry_date, title, note, activity_id))
        conexao.commit()
        return True
    finally:
        conexao.close()

def delete_process_activity(activity_id: int):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM process_activities WHERE id=?", (activity_id,))
        conexao.commit()
        return True
    finally:
        conexao.close()
