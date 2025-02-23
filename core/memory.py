# ~/VOTSai/core/memory.py
import sqlite3
from datetime import datetime
from collections import deque
from typing import Deque, Dict, Any
import logging

logger = logging.getLogger(__name__)

def init_memory_db(db_path: str = "vots_agi_memory.db") -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS long_term_memory
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      query TEXT NOT NULL,
                      answer TEXT NOT NULL,
                      timestamp TEXT NOT NULL,
                      tags TEXT,
                      model_used TEXT)''')
        c.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON long_term_memory (timestamp)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_query ON long_term_memory (query)")
        conn.commit()
        logger.info("Initialized memory database")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database initialization failed: {e}")
        raise

def update_memory(conn: sqlite3.Connection, query: str, result: Dict[str, Any], short_term_memory: Deque) -> None:
    try:
        short_term_memory.append({"query": query, "answer": result['answer'], "model": result['model_name']})
        if len(short_term_memory) > SHORT_TERM_MAX:
            oldest = short_term_memory.popleft()
            c = conn.cursor()
            c.execute("INSERT INTO long_term_memory (query, answer, timestamp, model_used) VALUES (?, ?, ?, ?)",
                      (oldest["query"], oldest["answer"], datetime.now().isoformat(), oldest["model"]))
            conn.commit()
    except Exception as e:
        logger.error(f"Memory update failed: {e}")

def get_relevant_memory(conn: sqlite3.Connection, query: str, limit: int = 3) -> str:
    try:
        c = conn.cursor()
        c.execute("SELECT query, answer, timestamp FROM long_term_memory WHERE query LIKE ? OR answer LIKE ? ORDER BY timestamp DESC LIMIT ?",
                  (f"%{query}%", f"%{query}%", limit))
        results = c.fetchall()
        if results:
            return "\n\n".join([f"**Past Query**: {row['query']}\n**Answer**: {row['answer']}\n**Timestamp**: {row['timestamp']}" for row in results])
        return "No relevant memory found."
    except Exception as e:
        logger.error(f"Memory retrieval failed: {e}")
        return f"Error retrieving memory: {e}"