"""
Vector Memory System for TRILOGY Brain

Implements a vector-based memory system with semantic search
"""
import os
import numpy as np
import sqlite3
import json
import logging
import time
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class VectorMemorySystem:
    """
    Vector-based memory system with semantic search capabilities
    
    This system:
    - Converts text to vector embeddings
    - Stores embeddings in SQLite database
    - Performs semantic search to find relevant memories
    - Implements intelligent memory pruning
    """
    
    def __init__(self, 
                db_path: str = "data/vector_memory.db", 
                model_name: str = "all-MiniLM-L6-v2",
                max_memories: int = 10000):
        """
        Initialize the vector memory system
        
        Args:
            db_path: Path to SQLite database file
            model_name: Name of the sentence transformer model to use
            max_memories: Maximum number of memories to store
        """
        self.db_path = db_path
        self.max_memories = max_memories
        
        # Create database directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize the embedding model
        try:
            self.model = SentenceTransformer(model_name)
            self.embedding_dim = self.model.get_sentence_embedding_dimension()
            logger.info(f"Initialized embedding model with dimension {self.embedding_dim}")
        except Exception as e:
            logger.error(f"Error initializing embedding model: {e}")
            raise
            
        # Initialize the database
        self._init_db()
    
    def _init_db(self) -> None:
        """Initialize the SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Create memories table
            c.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                response TEXT NOT NULL,
                embedding BLOB NOT NULL,
                timestamp TEXT NOT NULL,
                metadata TEXT,
                access_count INTEGER DEFAULT 0,
                last_access TEXT
            )
            ''')
            
            # Create index on timestamp
            c.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)")
            
            conn.commit()
            conn.close()
            
            logger.info("Vector memory database initialized")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    def add_memory(self, 
                  query: str, 
                  response: str, 
                  metadata: Optional[Dict[str, Any]] = None) -> int:
        """
        Add a memory to the system
        
        Args:
            query: User query or prompt
            response: Response or content to remember
            metadata: Additional information about the memory
            
        Returns:
            ID of the added memory
        """
        try:
            # Create a combined text for embedding
            text_to_embed = f"{query}\n\n{response}"
            
            # Generate embedding
            embedding = self.model.encode(text_to_embed)
            
            # Convert embedding to binary for storage
            embedding_bytes = embedding.tobytes()
            
            # Current timestamp
            timestamp = datetime.now().isoformat()
            
            # Convert metadata to JSON
            metadata_json = json.dumps(metadata) if metadata else None
            
            # Insert into database
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute('''
            INSERT INTO memories (query, response, embedding, timestamp, metadata)
            VALUES (?, ?, ?, ?, ?)
            ''', (query, response, embedding_bytes, timestamp, metadata_json))
            
            memory_id = c.lastrowid
            
            # Check if we need to prune memories
            c.execute("SELECT COUNT(*) FROM memories")
            count = c.fetchone()[0]
            
            if count > self.max_memories:
                self._prune_memories(c, count - self.max_memories)
            
            conn.commit()
            conn.close()
            
            logger.info(f"Added memory with ID {memory_id}")
            return memory_id
            
        except Exception as e:
            logger.error(f"Error adding memory: {e}")
            return -1
    
    def get_relevant_memories(self, 
                             query: str, 
                             limit: int = 5, 
                             min_similarity: float = 0.3) -> List[Dict[str, Any]]:
        """
        Retrieve memories relevant to the query
        
        Args:
            query: The query to find relevant memories for
            limit: Maximum number of memories to return
            min_similarity: Minimum similarity score (0-1)
            
        Returns:
            List of relevant memories
        """
        try:
            # Generate query embedding
            query_embedding = self.model.encode(query)
            
            # Get all memories from database
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT id, query, response, embedding, timestamp, metadata FROM memories")
            rows = c.fetchall()
            
            # Calculate similarity for each memory
            results = []
            for row in rows:
                memory_id, memory_query, response, embedding_bytes, timestamp, metadata_json = row
                
                # Convert binary to numpy array
                embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
                
                # Calculate cosine similarity
                similarity = np.dot(query_embedding, embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(embedding))
                
                if similarity >= min_similarity:
                    # Parse metadata
                    metadata = json.loads(metadata_json) if metadata_json else {}
                    
                    results.append({
                        "id": memory_id,
                        "query": memory_query,
                        "response": response,
                        "timestamp": timestamp,
                        "similarity": float(similarity),
                        "metadata": metadata
                    })
            
            # Update access count and last access time for retrieved memories
            if results:
                current_time = datetime.now().isoformat()
                for result in results:
                    c.execute('''
                    UPDATE memories
                    SET access_count = access_count + 1, last_access = ?
                    WHERE id = ?
                    ''', (current_time, result["id"]))
            
            conn.commit()
            conn.close()
            
            # Sort by similarity and return top matches
            results.sort(key=lambda x: x["similarity"], reverse=True)
            return results[:limit]
            
        except Exception as e:
            logger.error(f"Error retrieving relevant memories: {e}")
            return []
    
    def _prune_memories(self, cursor, count: int) -> None:
        """
        Prune least valuable memories
        
        Args:
            cursor: Database cursor
            count: Number of memories to prune
        """
        try:
            # Get all memories with their metrics
            cursor.execute('''
            SELECT id, timestamp, access_count, last_access
            FROM memories
            ''')
            
            memories = []
            for row in cursor.fetchall():
                memory_id, timestamp, access_count, last_access = row
                
                # Calculate age in days
                memory_time = datetime.fromisoformat(timestamp)
                age_days = (datetime.now() - memory_time).days
                
                # Calculate recency of access (days since last access)
                recency = 0
                if last_access:
                    last_access_time = datetime.fromisoformat(last_access)
                    recency = (datetime.now() - last_access_time).days
                else:
                    recency = age_days  # Never accessed
                
                # Calculate value score (higher = more valuable)
                # We value:
                # - Frequently accessed memories (higher access_count)
                # - Recently accessed memories (lower recency)
                # - Recent memories are protected somewhat (lower age penalty for newer memories)
                value = (access_count * 10) - (recency * 5) - (age_days * 0.5)
                
                memories.append((memory_id, value))
            
            # Sort by value (lowest first)
            memories.sort(key=lambda x: x[1])
            
            # Delete the least valuable memories
            to_delete = memories[:count]
            for memory_id, _ in to_delete:
                cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
                
            logger.info(f"Pruned {len(to_delete)} memories from the database")
            
        except Exception as e:
            logger.error(f"Error pruning memories: {e}") 