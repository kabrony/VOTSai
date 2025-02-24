import sqlite3
from datetime import datetime
from typing import Dict, Any, List, Optional, Deque
import logging

logger = logging.getLogger(__name__)

class MemoryService:
    """Service for memory-related database operations."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        self._connect()
        
    def _connect(self):
        """Connect to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self._initialize_db()
            logger.debug(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise
            
    def _initialize_db(self):
        """Initialize database schema if it doesn't exist."""
        try:
            c = self.conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS long_term_memory
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        query TEXT NOT NULL,
                        answer TEXT NOT NULL,
                        timestamp TEXT NOT NULL,
                        tags TEXT,
                        model_used TEXT)''')
            c.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON long_term_memory (timestamp)")
            c.execute("CREATE INDEX IF NOT EXISTS idx_query ON long_term_memory (query)")
            self.conn.commit()
            
            # Check for embeddings table, add if version > 1.0
            c.execute("PRAGMA table_info(memory_embeddings)")
            if not c.fetchall():
                c.execute('''CREATE TABLE IF NOT EXISTS memory_embeddings
                           (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            memory_id INTEGER NOT NULL,
                            embedding BLOB NOT NULL,
                            FOREIGN KEY (memory_id) REFERENCES long_term_memory (id))''')
                self.conn.commit()
                logger.info("Created memory_embeddings table")
        except sqlite3.Error as e:
            logger.error(f"Database initialization failed: {e}")
            raise
            
    def get_relevant_memories(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Get memories relevant to a query."""
        try:
            c = self.conn.cursor()
            c.execute("""
                SELECT id, query, answer, timestamp, tags, model_used 
                FROM long_term_memory 
                WHERE query LIKE ? OR answer LIKE ? 
                ORDER BY timestamp DESC LIMIT ?
            """, (f"%{query}%", f"%{query}%", limit))
            
            results = []
            for row in c.fetchall():
                results.append({
                    "id": row["id"],
                    "query": row["query"],
                    "answer": row["answer"],
                    "timestamp": row["timestamp"],
                    "tags": row["tags"].split(",") if row["tags"] else [],
                    "model_used": row["model_used"]
                })
                
            return results
        except sqlite3.Error as e:
            logger.error(f"Memory retrieval failed: {e}")
            return []
            
    def get_memories_by_date(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get memories within a date range."""
        try:
            c = self.conn.cursor()
            c.execute("""
                SELECT id, query, answer, timestamp, tags, model_used 
                FROM long_term_memory 
                WHERE timestamp BETWEEN ? AND ?
                ORDER BY timestamp DESC
            """, (start_date, end_date))
            
            results = []
            for row in c.fetchall():
                results.append({
                    "id": row["id"],
                    "query": row["query"],
                    "answer": row["answer"],
                    "timestamp": row["timestamp"],
                    "tags": row["tags"].split(",") if row["tags"] else [],
                    "model_used": row["model_used"]
                })
                
            return results
        except sqlite3.Error as e:
            logger.error(f"Memory date retrieval failed: {e}")
            return []
            
    def add_memory(self, query: str, answer: str, model_used: str = "", tags: List[str] = None) -> bool:
        """Add a new memory to the database."""
        try:
            c = self.conn.cursor()
            tags_str = ",".join(tags) if tags else ""
            timestamp = datetime.now().isoformat()
            
            c.execute("""
                INSERT INTO long_term_memory (query, answer, timestamp, tags, model_used)
                VALUES (?, ?, ?, ?, ?)
            """, (query, answer, timestamp, tags_str, model_used))
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Memory addition failed: {e}")
            self.conn.rollback()
            return False
            
    def update_memory_from_short_term(self, short_term_memory: Deque) -> None:
        """Update long-term memory from short-term memory."""
        if not short_term_memory:
            return
            
        oldest = short_term_memory.popleft()
        self.add_memory(
            query=oldest["query"],
            answer=oldest["answer"],
            model_used=oldest["model"],
            tags=oldest.get("tags", [])
        )
            
    def clear_memories(self) -> bool:
        """Clear all memories from the database."""
        try:
            c = self.conn.cursor()
            c.execute("DELETE FROM long_term_memory")
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Failed to clear memories: {e}")
            self.conn.rollback()
            return False
            
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            
    def __del__(self):
        """Ensure connection is closed on object destruction."""
        self.close() 