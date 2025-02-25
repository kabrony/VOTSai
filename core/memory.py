# ~/VOTSai/core/memory.py
import sqlite3
from datetime import datetime
from collections import deque
from typing import Deque, Dict, Any
import logging
import time
import numpy as np

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

class MemorySystem:
    """Enhanced memory system with improved retrieval and pruning"""
    
    def __init__(self, max_items=100):
        self.memories = []
        self.max_items = max_items
        self.embedding_model = EmbeddingModel()
        
    def add_memory(self, query, response, metadata=None):
        """Add a memory with automatic pruning if needed"""
        # Generate embedding for the query for future semantic search
        embedding = self.embedding_model.embed(query)
        
        memory = {
            "query": query,
            "response": response,
            "timestamp": time.time(),
            "embedding": embedding,
            "metadata": metadata or {}
        }
        
        self.memories.append(memory)
        
        # Prune if exceeding max_items
        if len(self.memories) > self.max_items:
            # Sort by importance score and remove least important
            importance_scores = self._calculate_importance_scores()
            delete_index = importance_scores.index(min(importance_scores))
            del self.memories[delete_index]
            
    def _calculate_importance_scores(self):
        """Calculate importance of each memory based on recency and uniqueness"""
        now = time.time()
        scores = []
        
        for memory in self.memories:
            # Recency factor - more recent = more important
            recency = 1.0 / (1.0 + 0.01 * (now - memory["timestamp"]))
            
            # Uniqueness factor - more unique = more important
            uniqueness = self._calculate_uniqueness(memory)
            
            # Combined score
            scores.append(recency * 0.7 + uniqueness * 0.3)
            
        return scores
        
    def _calculate_uniqueness(self, target_memory):
        """Calculate how unique a memory is compared to others"""
        if len(self.memories) <= 1:
            return 1.0
            
        target_embedding = target_memory["embedding"]
        similarities = []
        
        for memory in self.memories:
            if memory is target_memory:
                continue
                
            other_embedding = memory["embedding"]
            similarity = np.dot(target_embedding, other_embedding)
            similarities.append(similarity)
            
        # Average similarity (lower is more unique)
        avg_similarity = sum(similarities) / len(similarities)
        # Convert to uniqueness (higher is more unique)
        return 1.0 - avg_similarity
        
    def find_relevant_memories(self, query, limit=3):
        """Find most semantically relevant memories to the query"""
        if not self.memories:
            return []
            
        query_embedding = self.embedding_model.embed(query)
        
        # Calculate similarities
        similarities = []
        for memory in self.memories:
            memory_embedding = memory["embedding"]
            similarity = np.dot(query_embedding, memory_embedding)
            similarities.append((memory, similarity))
            
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top matches
        return [memory for memory, _ in similarities[:limit]]