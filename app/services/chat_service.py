import sqlite3
from pathlib import Path
from typing import List, Optional, Dict

class ChatService:
    def __init__(self):
        self.db_path = Path(__file__).parent.parent.parent / "infrastructure" / "database" / "compromissos.sqlite"
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message TEXT NOT NULL,
                    role TEXT NOT NULL,
                    chat_id INTEGER NOT NULL,
                    FOREIGN KEY(chat_id) REFERENCES chats(id) ON DELETE CASCADE
                )
            """)
            conn.commit()

    def criar_chat(self, title: str) -> Dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("INSERT INTO chats (title) VALUES (?)", (title,))
            conn.commit()
            return {"id": cursor.lastrowid, "title": title}

    def obter_chat(self, chat_id: int) -> Optional[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM chats WHERE id = ?", (chat_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def listar_chats(self) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM chats ORDER BY id DESC")
            return [dict(row) for row in cursor.fetchall()]

    def deletar_chat(self, chat_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.execute("DELETE FROM chats WHERE id = ?", (chat_id,))
            conn.commit()
            return cursor.rowcount > 0

    def adicionar_interacao(self, chat_id: int, message: str, role: str) -> Dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO messages (message, role, chat_id) VALUES (?, ?, ?)",
                (message, role, chat_id)
            )
            conn.commit()
            return {
                "id": cursor.lastrowid,
                "message": message,
                "role": role,
                "chat_id": chat_id
            }

    def listar_interacoes(self, chat_id: int) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM messages WHERE chat_id = ? ORDER BY id ASC",
                (chat_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
        
    def listar_ultimas_10_interacoes(self, chat_id: int) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM messages WHERE chat_id = ? ORDER BY id DESC LIMIT 10",
                (chat_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
