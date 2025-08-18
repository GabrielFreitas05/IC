from db.db import conectar

def insert_update(processo_id, tipo, descricao=None, valor=None, unidade=None, autor_id=None, anexo_path=None):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO processo_updates (processo_id, tipo, descricao, valor, unidade, autor_id, anexo_path)
        VALUES (?,?,?,?,?,?,?)
    """, (processo_id, tipo, descricao, valor, unidade, autor_id, anexo_path))
    conn.commit()
    conn.close()

def list_updates_by_processo(processo_id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT strftime('%d/%m/%Y %H:%M', coletado_em), tipo,
               COALESCE(descricao,'') ||
               CASE WHEN valor IS NOT NULL THEN ' ['||printf('%.2f',valor)||COALESCE(' '||unidade,'')||']' ELSE '' END
        FROM processo_updates
        WHERE processo_id=?
        ORDER BY datetime(coletado_em) DESC, id DESC
    """, (processo_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def finish_process(processo_id, resultado=None, tempo_real_min=None, qualidade=None, licoes=None, autor_id=None):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("UPDATE formularios_processos SET status='Concluido', data_fim=CURRENT_TIMESTAMP WHERE id=?", (processo_id,))
    cur.execute("INSERT INTO processo_updates (processo_id, tipo, descricao, autor_id) VALUES (?,?,?,?)", (processo_id, 'fechamento_resultado', resultado, autor_id))
    cur.execute("INSERT INTO processo_updates (processo_id, tipo, valor, unidade, descricao, autor_id) VALUES (?,?,?,?,?,?)", (processo_id, 'fechamento_tempo', tempo_real_min, 'min', 'Tempo real de execução', autor_id))
    cur.execute("INSERT INTO processo_updates (processo_id, tipo, valor, unidade, descricao, autor_id) VALUES (?,?,?,?,?,?)", (processo_id, 'fechamento_qualidade', qualidade, 'pts', 'Qualidade final', autor_id))
    cur.execute("INSERT INTO processo_updates (processo_id, tipo, descricao, autor_id) VALUES (?,?,?,?)", (processo_id, 'fechamento_licoes', licoes, autor_id))
    try:
        cur.execute("INSERT INTO indicadores (processo_id, etapa_id, nome, unidade, meta, valor, coletado_em, coletado_por) VALUES (?,?,?,?,?,?,CURRENT_TIMESTAMP,?)", (processo_id, None, 'Tempo médio (min)', 'min', None, tempo_real_min, autor_id))
        cur.execute("INSERT INTO indicadores (processo_id, etapa_id, nome, unidade, meta, valor, coletado_em, coletado_por) VALUES (?,?,?,?,?,?,CURRENT_TIMESTAMP,?)", (processo_id, None, 'Qualidade (nota)', 'pts', None, qualidade, autor_id))
    except:
        pass
    conn.commit()
    conn.close()
