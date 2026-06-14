import sqlite3
from pathlib import Path

class LogsService:
    def __init__(self):
        self.db_path = Path(__file__).parent.parent.parent / "infrastructure" / "database" / "compromissos.sqlite"
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pergunta TEXT NOT NULL,
                    resposta TEXT,
                    tool TEXT,
                    criado_em TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    

    def salvar_log(self, pergunta: str, resposta: str, tool: str) -> dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO logs (pergunta, resposta, tool)
                VALUES (?, ?, ?)
            """, (pergunta, resposta, tool))
            conn.commit()
            return {
                "id": cursor.lastrowid,
                "pergunta": pergunta,
                "resposta": resposta,
                "tool": tool
            }