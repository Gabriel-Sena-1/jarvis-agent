import sqlite3
from pathlib import Path
from typing import List, Optional, Dict

class RecallService:
    def __init__(self):
        self.db_path = Path(__file__).parent.parent.parent / "infrastructure" / "database" / "compromissos.sqlite"
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS historico_recall (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    documento TEXT NOT NULL,
                    pergunta TEXT NOT NULL,
                    resposta_usuario TEXT,
                    avaliacao TEXT, -- 'correta' | 'parcial' | 'incorreta'
                    resposta_correta TEXT,
                    criado_em TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def salvar_pergunta_recall(self, documento: str, pergunta: str, resposta_correta: str) -> dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO historico_recall (documento, pergunta, resposta_correta)
                VALUES (?, ?, ?)
            """, (documento, pergunta, resposta_correta))
            conn.commit()
            return {
                "id": cursor.lastrowid,
                "documento": documento,
                "pergunta": pergunta,
                "resposta_correta": resposta_correta
            }

    def obter_recall_pendente(self) -> Optional[dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM historico_recall
                WHERE resposta_usuario IS NULL
                ORDER BY id ASC LIMIT 1
            """)
            row = cursor.fetchone()
            return dict(row) if row else None

    def atualizar_resposta_recall(self, id: int, resposta_usuario: str, avaliacao: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE historico_recall
                SET resposta_usuario = ?, avaliacao = ?
                WHERE id = ?
            """, (resposta_usuario, avaliacao, id))
            conn.commit()

    def obter_ultimas_perguntas(self, limite: int = 5) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM historico_recall
                ORDER BY id DESC LIMIT ?
            """, (limite,))
            return [dict(row) for row in cursor.fetchall()]

    def listar_recall_com_erros(self) -> list:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT documento, pergunta, avaliacao
                FROM historico_recall
                ORDER BY criado_em DESC LIMIT 100
            ''')
            return [dict(r) for r in cursor.fetchall()]
