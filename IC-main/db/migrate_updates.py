import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'usuarios.db')
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys=ON")
cur.execute("""
CREATE TABLE IF NOT EXISTS processo_updates (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  processo_id INTEGER NOT NULL,
  tipo TEXT NOT NULL,
  descricao TEXT,
  valor REAL,
  unidade TEXT,
  coletado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  autor_id INTEGER,
  anexo_path TEXT,
  FOREIGN KEY (processo_id) REFERENCES formularios_processos(id)
)
""")
cols = [r[1] for r in cur.execute("PRAGMA table_info(formularios_processos)").fetchall()]
if "status" not in cols:
    cur.execute("ALTER TABLE formularios_processos ADD COLUMN status TEXT")
if "data_fim" not in cols:
    cur.execute("ALTER TABLE formularios_processos ADD COLUMN data_fim TIMESTAMP")
conn.commit()
conn.close()
print("OK")
