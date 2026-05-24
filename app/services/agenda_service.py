import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict


class AgendaService:
    def __init__(self):
        self.db_path = Path(__file__).parent.parent.parent / "infrastructure" / "database" / "compromissos.sqlite"
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS compromissos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    data TEXT NOT NULL,
                    horario TEXT NOT NULL,
                    descricao TEXT,
                    finished_at TEXT,
                    criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
                    atualizado_em TEXT
                )
            """)
            # migração: adiciona coluna se já existir tabela sem ela
            try:
                conn.execute("ALTER TABLE compromissos ADD COLUMN finished_at TEXT")
            except Exception:
                pass
            conn.commit()
    
    def criar(self, nome: str, data: str, horario: str, descricao: str = "") -> Dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO compromissos (nome, data, horario, descricao)
                VALUES (?, ?, ?, ?)
            """, (nome, data, horario, descricao))
            conn.commit()
            
            id_novo = cursor.lastrowid
            return self._get_by_id(id_novo)
    
    def listar(self, data: Optional[str] = None) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            if data:
                cursor = conn.execute("""
                    SELECT * FROM compromissos
                    WHERE data = ?
                    ORDER BY horario ASC
                """, (data,))
            else:
                cursor = conn.execute("""
                    SELECT * FROM compromissos
                    ORDER BY data ASC, horario ASC
                """)
            
            return [dict(row) for row in cursor.fetchall()]
    
    def atualizar(self, id: int, nome: str = None, data: str = None, 
                  horario: str = None, descricao: str = None) -> Optional[Dict]:
        updates = []
        params = []
        
        if nome is not None:
            updates.append("nome = ?")
            params.append(nome)
        if data is not None:
            updates.append("data = ?")
            params.append(data)
        if horario is not None:
            updates.append("horario = ?")
            params.append(horario)
        if descricao is not None:
            updates.append("descricao = ?")
            params.append(descricao)
        
        if not updates:
            return self._get_by_id(id)
        
        updates.append("atualizado_em = CURRENT_TIMESTAMP")
        params.append(id)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(f"""
                UPDATE compromissos
                SET {', '.join(updates)}
                WHERE id = ?
            """, params)
            conn.commit()
        
        return self._get_by_id(id)
    
    def deletar(self, id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM compromissos WHERE id = ?", (id,))
            conn.commit()
            return cursor.rowcount > 0

    def concluir(self, id: int) -> Optional[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE compromissos
                SET finished_at = CURRENT_TIMESTAMP, atualizado_em = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (id,))
            conn.commit()
        return self._get_by_id(id)
    
    def _get_by_id(self, id: int) -> Optional[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM compromissos WHERE id = ?
            """, (id,))
            row = cursor.fetchone()
            return dict(row) if row else None
