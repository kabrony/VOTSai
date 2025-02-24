import tiktoken
import hashlib
from functools import lru_cache
import logging
from typing import Dict, Optional, Tuple, List

logger = logging.getLogger(__name__)

class TokenManager:
    """Efficiently manage and count tokens for various models."""
    
    # Map model families to tiktoken encodings
    MODEL_ENCODINGS = {
        "perplexity": "cl100k_base",  # Perplexity uses OpenAI tokenization
        "deepseek": "cl100k_base",    # DeepSeek similar to GPT-4
        "claude": "cl100k_base",      # Claude uses Anthropic's tokenizer
        "local": "cl100k_base",       # Local models vary, use common encoding
    }
    
    @staticmethod
    def _get_model_family(model_name: str) -> str:
        """Determine the model family based on the model name."""
        model_name = model_name.lower()
        if "perplexity" in model_name:
            return "perplexity"
        elif "deepseek" in model_name:
            return "deepseek"
        elif "claude" in model_name:
            return "claude"
        else:
            return "local"
    
    @staticmethod
    @lru_cache(maxsize=128)
    def _get_encoding(model_family: str) -> tiktoken.Encoding:
        """Get the encoding for a model family with caching."""
        encoding_name = TokenManager.MODEL_ENCODINGS.get(model_family, "cl100k_base")
        try:
            return tiktoken.get_encoding(encoding_name)
        except Exception as e:
            logger.warning(f"Error getting tiktoken encoding {encoding_name}: {e}")
            # Fallback to cl100k_base (GPT-4 encoding)
            return tiktoken.get_encoding("cl100k_base")
    
    @staticmethod
    @lru_cache(maxsize=1024)
    def _cached_count_tokens(text_hash: str, model_family: str) -> int:
        """Count tokens with hash-based caching."""
        # This is a helper for the count_tokens method - not called directly
        encoding = TokenManager._get_encoding(model_family)
        return len(encoding.encode(TokenManager._cached_count_tokens._text))
    
    @staticmethod
    def count_tokens(text: str, model_name: str) -> int:
        """Count the number of tokens in text for a specific model."""
        if not text:
            return 0
            
        model_family = TokenManager._get_model_family(model_name)
        
        # Generate a hash of the text to use as a cache key
        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        
        # Store the text in the function to access it in _cached_count_tokens
        TokenManager._cached_count_tokens._text = text
        
        # Call the cached function
        return TokenManager._cached_count_tokens(text_hash, model_family)
    
    @staticmethod
    def truncate_to_tokens(text: str, max_tokens: int, model_name: str) -> str:
        """Truncate text to fit within max_tokens."""
        if not text:
            return ""
            
        try:
            model_family = TokenManager._get_model_family(model_name)
            encoding = TokenManager._get_encoding(model_family)
            tokens = encoding.encode(text)
            
            if len(tokens) <= max_tokens:
                return text
                
            truncated_tokens = tokens[:max_tokens]
            return encoding.decode(truncated_tokens)
        except Exception as e:
            logger.error(f"Error truncating text: {e}")
            # Fallback to character-based truncation (very approximate)
            avg_chars_per_token = 4
            safe_char_count = int(max_tokens * avg_chars_per_token * 0.9)
            return text[:safe_char_count]
    
    @staticmethod
    def split_into_chunks(text: str, chunk_size: int, model_name: str, overlap: int = 0) -> List[str]:
        """Split text into chunks of roughly chunk_size tokens with optional overlap."""
        if not text:
            return []
            
        try:
            model_family = TokenManager._get_model_family(model_name)
            encoding = TokenManager._get_encoding(model_family)
            tokens = encoding.encode(text)
            
            chunks = []
            for i in range(0, len(tokens), chunk_size - overlap):
                chunk_tokens = tokens[i:i + chunk_size]
                chunk_text = encoding.decode(chunk_tokens)
                chunks.append(chunk_text)
                
                # If we've processed all tokens, break
                if i + chunk_size >= len(tokens):
                    break
                    
            return chunks
        except Exception as e:
            logger.error(f"Error splitting text into chunks: {e}")
            
            # Fallback: rough chunking based on characters
            words = text.split()
            avg_tokens_per_word = 4 / 3  # rough estimate
            words_per_chunk = int(chunk_size / avg_tokens_per_word)
            overlap_words = int(overlap / avg_tokens_per_word)
            
            chunks = []
            for i in range(0, len(words), words_per_chunk - overlap_words):
                chunk = " ".join(words[i:i + words_per_chunk])
                chunks.append(chunk)
                
                # If we've processed all words, break
                if i + words_per_chunk >= len(words):
                    break
                    
            return chunks
            
    @staticmethod
    def estimate_cost(input_tokens: int, output_tokens: int, model_name: str) -> float:
        """Estimate the cost of a query in USD."""
        # Simplified cost model - should be updated with actual pricing
        costs = {
            "perplexity": {"input": 0.0000005, "output": 0.0000015},
            "deepseek": {"input": 0.0000010, "output": 0.0000020},
            "claude": {"input": 0.0000015, "output": 0.0000060},
            "local": {"input": 0, "output": 0}  # Local models are free
        }
        
        model_family = TokenManager._get_model_family(model_name)
        cost_rates = costs.get(model_family, {"input": 0, "output": 0})
        
        return (input_tokens * cost_rates["input"]) + (output_tokens * cost_rates["output"]) 