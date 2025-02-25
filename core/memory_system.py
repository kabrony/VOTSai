"""
Memory System Module

Maintains conversation history and provides contextual retrieval
for the TRILOGY Brain system.
"""
import logging
import time
from typing import Dict, Any, List, Optional
import os
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class MemorySystem:
    """
    Memory system for storing and retrieving conversation context
    
    This system:
    - Stores conversation history
    - Retrieves relevant context for new queries
    - Manages memory pruning and organization
    """
    
    def __init__(self, max_items: int = 100):
        """
        Initialize the memory system
        
        Args:
            max_items: Maximum number of memories to store
        """
        self.memories = []
        self.max_items = max_items
        logger.info(f"Memory system initialized with capacity for {max_items} items")
        
    def add_memory(self, query: str, response: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a new memory
        
        Args:
            query: The user query
            response: The system response
            metadata: Additional information about the interaction
        """
        memory = {
            "query": query,
            "response": response,
            "text": f"Query: {query}\nResponse: {response}",
            "timestamp": time.time(),
            "metadata": metadata or {}
        }
        
        # Add to memory
        self.memories.append(memory)
        
        # Prune if needed
        if len(self.memories) > self.max_items:
            # Remove oldest memory
            self.memories.pop(0)
            
        logger.debug(f"Added memory: {query[:50]}...")
        
    def get_relevant_memories(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Get memories relevant to the current query
        
        Args:
            query: The current query
            limit: Maximum number of memories to return
            
        Returns:
            List of relevant memories
        """
        if not self.memories:
            return []
            
        # Simple relevance based on keyword matching
        # This could be enhanced with embeddings for semantic search
        query_words = set(query.lower().split())
        
        # Calculate relevance scores
        scored_memories = []
        for memory in self.memories:
            # Count matching words
            memory_text = (memory["query"] + " " + memory["response"]).lower()
            memory_words = set(memory_text.split())
            
            # Calculate intersection and relevance score
            matching_words = query_words.intersection(memory_words)
            score = len(matching_words) / max(1, len(query_words))
            
            # Add recency factor (more recent = higher score)
            age = time.time() - memory["timestamp"]
            recency_factor = 1.0 / (1.0 + (age / 86400))  # 86400 seconds in a day
            
            final_score = score * 0.7 + recency_factor * 0.3
            
            scored_memories.append((memory, final_score))
        
        # Sort by score and return top matches
        scored_memories.sort(key=lambda x: x[1], reverse=True)
        return [memory for memory, _ in scored_memories[:limit]]
        
    def clear_memories(self) -> None:
        """Clear all memories"""
        self.memories = []
        logger.info("Memory system cleared")
        
    def save_memories(self, filepath: str) -> None:
        """
        Save memories to a file
        
        Args:
            filepath: Path to save the memories
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w') as f:
                json.dump(self.memories, f, indent=2)
                
            logger.info(f"Saved {len(self.memories)} memories to {filepath}")
        except Exception as e:
            logger.error(f"Error saving memories: {e}")
            
    def load_memories(self, filepath: str) -> bool:
        """
        Load memories from a file
        
        Args:
            filepath: Path to load the memories from
            
        Returns:
            Success flag
        """
        if not os.path.exists(filepath):
            logger.warning(f"Memory file not found: {filepath}")
            return False
            
        try:
            with open(filepath, 'r') as f:
                memories = json.load(f)
                
            # Validate and load memories
            valid_memories = []
            for memory in memories:
                if "query" in memory and "response" in memory:
                    # Add text field if missing
                    if "text" not in memory:
                        memory["text"] = f"Query: {memory['query']}\nResponse: {memory['response']}"
                    valid_memories.append(memory)
                    
            self.memories = valid_memories[:self.max_items]
            logger.info(f"Loaded {len(self.memories)} memories from {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error loading memories: {e}")
            return False
            
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the memory system
        
        Returns:
            Dictionary with memory statistics
        """
        if not self.memories:
            return {
                "count": 0,
                "oldest": None,
                "newest": None,
                "avg_query_length": 0,
                "avg_response_length": 0
            }
            
        # Calculate statistics
        timestamps = [m["timestamp"] for m in self.memories]
        query_lengths = [len(m["query"]) for m in self.memories]
        response_lengths = [len(m["response"]) for m in self.memories]
        
        return {
            "count": len(self.memories),
            "oldest": min(timestamps),
            "newest": max(timestamps),
            "avg_query_length": sum(query_lengths) / len(query_lengths),
            "avg_response_length": sum(response_lengths) / len(response_lengths)
        }

    # Add compatibility methods for VectorMemorySystem interface
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the memory system
        
        Returns:
            Dictionary of memory statistics
        """
        if not self.memories:
            return {
                "count": 0,
                "oldest": None,
                "newest": None,
                "types": {}
            }
            
        timestamps = [datetime.fromisoformat(m.get("timestamp", datetime.now().isoformat())) 
                      for m in self.memories]
                      
        return {
            "count": len(self.memories),
            "oldest": min(timestamps).isoformat() if timestamps else None,
            "newest": max(timestamps).isoformat() if timestamps else None,
            "types": {"conversation": len(self.memories)}
        }
        
    def search_memories(self, search_text: str, filters: Optional[Dict[str, Any]] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search memories by text and filters
        
        Args:
            search_text: Text to search for
            filters: Metadata filters
            limit: Maximum number of results
            
        Returns:
            List of matching memories
        """
        results = []
        
        for memory in reversed(self.memories):  # Most recent first
            # Simple text search
            if search_text.lower() in memory.get("query", "").lower() or search_text.lower() in memory.get("response", "").lower():
                # Apply filters if provided
                if filters:
                    # Check if all filters match
                    if all(memory.get("metadata", {}).get(k) == v for k, v in filters.items()):
                        results.append(memory)
                else:
                    results.append(memory)
                    
            # Stop if we have enough results
            if len(results) >= limit:
                break
                
        return results
        
    def delete_memory(self, memory_id: str) -> bool:
        """
        Delete a memory by ID
        
        Args:
            memory_id: ID of memory to delete
            
        Returns:
            Success status
        """
        for i, memory in enumerate(self.memories):
            if memory.get("id") == memory_id:
                self.memories.pop(i)
                return True
                
        return False 