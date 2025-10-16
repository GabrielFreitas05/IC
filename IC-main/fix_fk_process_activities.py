import sqlite3
import os

DB_PATH = "usuarios.db"  # ajuste se seu arquivo estiver em outro lugar

def fk_info(conn):
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_key_list(process_activities);")
    return cur.fetchall()

def table_exists(conn, name):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (name,))
    return cur.fetchone() is not None

def main():
    if not os.path.exists(DB_PATH):
        raise SystemExit(f"Banco não encontrado em: {os.path.abspath(DB_PATH)}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Ver FK atual
    cur.execute("PRAGMA foreign_keys = ON;")
    before = fk_info(conn)
    print("FK atual:", before)

    # Se já estiver correta, só sai
    needs_fix = True
    for row in before:
        # PRAGMA foreign_key_list: (id, seq, table, from, to, on_update, on_delete, match)
        # Queremos 'table' == 'formularios_processos'
        if len(row) >= 3 and row[2] == "formularios_processos":
            needs_fix = False
            break

    if not needs_fix and before:
        print("✅ A FK já aponta para formularios_processos(id). Nada a fazer.")
        conn.close()
        return

    print("⚙️  Recriando a tabela process_activities com FK para formularios_processos(id)...")

    # Desliga FK p/ migração
    cur.execute("PRAGMA foreign_keys = OFF;")
    conn.commit()

    # Se não existir ainda, só cria do zero
    if not table_exists(conn, "process_activities"):
        cur.executescript("""
        CREATE TABLE process_activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            process_id INTEGER NOT NULL,
            entry_date TEXT NOT NULL,
            title TEXT NOT NULL,
            note TEXT,
            author_id INTEGER,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (process_id) REFERENCES formularios_processos(id) ON DELETE CASCADE
        );
        """)
        conn.commit()
        print("✅ Tabela criada do zero com FK correta.")
    else:
        # Criar tabela nova com FK correta
        cur.executescript("""
        BEGIN TRANSACTION;

        CREATE TABLE process_activities_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            process_id INTEGER NOT NULL,
            entry_date TEXT NOT NULL,
            title TEXT NOT NULL,
            note TEXT,
            author_id INTEGER,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (process_id) REFERENCES formularios_processos(id) ON DELETE CASCADE
        );

        COMMIT;
        """)
        conn.commit()

        # Copiar apenas registros que tenham process_id existente em formularios_processos
        # (isso evita estourar FK ao migrar)
        cur.executescript("""
        INSERT INTO process_activities_new (id, process_id, entry_date, title, note, author_id, created_at, updated_at)
        SELECT pa.id, pa.process_id, pa.entry_date, pa.title, pa.note, pa.author_id, pa.created_at, pa.updated_at
        FROM process_activities pa
        WHERE pa.process_id IN (SELECT id FROM formularios_processos);
        """)
        conn.commit()

        # Troca as tabelas
        cur.executescript("""
        DROP TABLE process_activities;
        ALTER TABLE process_activities_new RENAME TO process_activities;
        """)
        conn.commit()
        print("✅ Dados válidos migrados e FK corrigida.")

    # Liga FK de volta e confirma
    cur.execute("PRAGMA foreign_keys = ON;")
    conn.commit()
    after = fk_info(conn)
    print("FK depois:", after)

    # Validação simples
    ok = any(len(r) >= 3 and r[2] == "formularios_processos" for r in after)
    print("✅ Verificação final:", "OK" if ok else "NÃO OK")
    conn.close()

if __name__ == "__main__":
    main()
