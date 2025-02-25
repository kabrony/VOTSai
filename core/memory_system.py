import logging
import time
import json
import os
from typing import Dict, Any, List
import sqlite3
import numpy as np

logger = logging.getLogger(__name__)

class MemorySystem:
    """Advanced memory management system for VOTSai"""
    
    def __init__(self, embedding_model, db_path="memory.db"):
        self.embedding_model = embedding_model
        self.db_path = db_path
        
        # Initialize databases
        self.init_database()
        
        # Short-term memory (recent interactions, kept in RAM)
        self.short_term = []
        self.short_term_max = 50
        
        logger.info("Memory system initialized")
    
    def init_database(self):
        """Initialize the SQLite database for long-term storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create memory table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            response TEXT NOT NULL,
            embedding BLOB NOT NULL,
            timestamp REAL NOT NULL,
            metadata TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info(f"Memory database initialized at {self.db_path}")
    
    def add(self, query: str, result: Dict[str, Any]):
        """
        Add a new memory entry
        """
        # Extract the response text
        response = result.get("answer", "")
        
        # Get current timestamp
        timestamp = time.time()
        
        # Generate embedding for the combined query + response
        combined_text = f"{query} {response}"
        embedding = self.embedding_model.embed(combined_text)
        
        # Prepare metadata
        metadata = {
            "model": result.get("model", "unknown"),
            "latency": result.get("latency", 0),
            "tokens": {
                "input": result.get("input_tokens", 0),
                "output": result.get("output_tokens", 0)
            }
        }
        
        # Add to short-term memory
        self.short_term.append({
            "query": query,
            "response": response,
            "embedding": embedding,
            "timestamp": timestamp,
            "metadata": metadata
        })
        
        # Trim short-term memory if needed
        if len(self.short_term) > self.short_term_max:
            self.short_term = self.short_term[-self.short_term_max:]
        
        # Add to long-term database
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO memories (query, response, embedding, timestamp, metadata) VALUES (?, ?, ?, ?, ?)",
                (query, response, embedding.tobytes(), timestamp, json.dumps(metadata))
            )
            
            conn.commit()
            conn.close()
            
            logger.info(f"Added new memory: {query[:50]}...")
        except Exception as e:
            logger.error(f"Failed to add memory to database: {e}")
    
    def retrieve_relevant(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve memories relevant to the query
        """
        # Generate embedding for query
        query_embedding = self.embedding_model.embed(query)
        
        # Search short-term memory
        short_term_results = self._search_short_term(query_embedding, limit)
        
        # Search long-term memory
        long_term_results = self._search_long_term(query_embedding, limit)
        
        # Combine and rank results
        combined_results = self._rank_results(short_term_results, long_term_results)
        
        # Return top results
        return combined_results[:limit]
    
    def _search_short_term(self, query_embedding, limit: int = 5):
        """Search short-term memory for relevant entries"""
        results = []
        
        for memory in self.short_term:
            # Calculate similarity
            similarity = self._cosine_similarity(query_embedding, memory["embedding"])
            
            # Add to results if similarity is above threshold
            if similarity > 0.5:  # Threshold can be adjusted
                results.append({
                    "query": memory["query"],
                    "response": memory["response"],
                    "similarity": similarity,
                    "timestamp": memory["timestamp"],
                    "source": "short_term"
                })
        
        # Sort by similarity
        results.sort(key=lambda x: x["similarity"], reverse=True)
        
        return results[:limit]
    
    def _search_long_term(self, query_embedding, limit: int = 5):
        """Search long-term memory for relevant entries"""
        results = []
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get all memories from database
            cursor.execute("SELECT id, query, response, embedding, timestamp, metadata FROM memories")
            rows = cursor.fetchall()
            
            # Calculate similarities
            for row in rows:
                memory_id, query, response, embedding_bytes, timestamp, metadata_json = row
                
                # Convert embedding bytes to numpy array
                memory_embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
                
                # Calculate similarity
                similarity = self._cosine_similarity(query_embedding, memory_embedding)
                
                # Add to results if similarity is above threshold
                if similarity > 0.5:  # Threshold can be adjusted
                    results.append({
                        "query": query,
                        "response": response,
                        "similarity": similarity,
                        "timestamp": timestamp,
                        "source": "long_term",
                        "metadata": json.loads(metadata_json) if metadata_json else {}
                    })
            
            conn.close()
            
            # Sort by similarity
            results.sort(key=lambda x: x["similarity"], reverse=True)
            
            return results[:limit]
            
        except Exception as e:
            logger.error(f"Failed to search long-term memory: {e}")
            return []
    
    def _rank_results(self, short_term_results, long_term_results):
        """Combine and rank results from different memory sources"""
        # Combine results
        combined = short_term_results + long_term_results
        
        # Sort by similarity
        combined.sort(key=lambda x: x["similarity"], reverse=True)
        
        return combined
    
    def _cosine_similarity(self, embedding1, embedding2):
        """Calculate cosine similarity between two embeddings"""
        dot_product = np.dot(embedding1, embedding2)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return dot_product / (norm1 * norm2)
    
    def clear_short_term(self):
        """Clear short-term memory"""
        self.short_term = []
        logger.info("Short-term memory cleared")
    
    def clear_all(self):
        """Clear all memory (use with caution)"""
        self.clear_short_term()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM memories")
            
            conn.commit()
            conn.close()
            
            logger.info("All memory cleared")
        except Exception as e:
            logger.error(f"Failed to clear long-term memory: {e}") 