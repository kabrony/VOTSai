import numpy as np
import logging

logger = logging.getLogger(__name__)

class EmbeddingModel:
    """Simple embedding model that creates consistent embeddings based on text hash"""
    
    def __init__(self):
        self.dimensions = 384
        logger.info(f"Initialized embedding model with {self.dimensions} dimensions")
    
    def embed(self, text):
        """
        Create a deterministic embedding vector based on the text
        This is a stub implementation for testing
        """
        # Use hash of text to seed the random generator for consistent vectors
        np.random.seed(hash(text) % 2**32)
        
        # Generate a random vector
        embedding = np.random.rand(self.dimensions).astype(np.float32)
        
        # Reset the random seed to avoid affecting other random operations
        np.random.seed(None)
        
        return embedding