BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE,
  role TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS processes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  start_date TEXT,
  status TEXT,
  owner_id INTEGER,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(owner_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS process_steps (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  process_id INTEGER NOT NULL,
  step_order INTEGER NOT NULL,
  name TEXT NOT NULL,
  status TEXT,
  started_at TEXT,
  finished_at TEXT,
  FOREIGN KEY(process_id) REFERENCES processes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS pops (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code TEXT NOT NULL,
  version TEXT NOT NULL,
  issued_at TEXT,
  owner_id INTEGER,
  title TEXT,
  FOREIGN KEY(owner_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS pop_revisions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pop_id INTEGER NOT NULL,
  version TEXT NOT NULL,
  changed_by INTEGER,
  changed_at TEXT DEFAULT CURRENT_TIMESTAMP,
  changes_text TEXT,
  FOREIGN KEY(pop_id) REFERENCES pops(id) ON DELETE CASCADE,
  FOREIGN KEY(changed_by) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS ptas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  date TEXT NOT NULL,
  description TEXT,
  actions TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS attachments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  owner_table TEXT NOT NULL,
  owner_id INTEGER NOT NULL,
  file_path TEXT NOT NULL,
  type TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_processes_owner ON processes(owner_id);
CREATE INDEX IF NOT EXISTS idx_steps_process ON process_steps(process_id, step_order);
CREATE INDEX IF NOT EXISTS idx_pta_user_date ON ptas(user_id, date);
CREATE INDEX IF NOT EXISTS idx_pops_code_version ON pops(code, version);

COMMIT;