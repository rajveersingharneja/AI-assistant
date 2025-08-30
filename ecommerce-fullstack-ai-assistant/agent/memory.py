import sqlite3
from typing import List, Tuple

DB_PATH = 'assistant.db'

INIT_SQL = """
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('system','user','assistant','tool')),
    content TEXT NOT NULL,
    ts DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

class MemoryStore:
    def __init__(self, path: str = DB_PATH):
        self.path = path
        self._ensure()

    def _ensure(self):
        with sqlite3.connect(self.path) as con:
            con.execute(INIT_SQL)

    def add(self, user_id: str, role: str, content: str):
        with sqlite3.connect(self.path) as con:
            con.execute("INSERT INTO messages (user_id, role, content) VALUES (?,?,?)",
                        (user_id, role, content))

    def history(self, user_id: str, limit: int = 20) -> List[Tuple[str,str]]:
        with sqlite3.connect(self.path) as con:
            rows = con.execute(
                "SELECT role, content FROM messages WHERE user_id=? ORDER BY id DESC LIMIT ?",
                (user_id, limit)
            ).fetchall()
        # return chronological
        return list(reversed(rows))

    def clear(self, user_id: str):
        with sqlite3.connect(self.path) as con:
            con.execute("DELETE FROM messages WHERE user_id=?", (user_id,))
