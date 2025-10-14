import sqlite3
from pathlib import Path

def _default_db_path():
    here = Path(__file__).resolve()
    project_root = here.parent.parent
    db_path = project_root / "usuarios.db"
    return db_path.as_posix()

def get_connection(db_path=None):
    path = db_path or _default_db_path()
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn
