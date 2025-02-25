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
        "perplexity": "gpt-3.5-turbo",
        "deepseek": "gpt-3.5-turbo",  # Approximation
        "claude": "cl100k_base",
        "local": None  # Local models use fallback counting
    }
    
    @staticmethod
    @lru_cache(maxsize=1024)
    def _get_encoding(model_family: str) -> Optional[tiktoken.Encoding]:
        """Get the appropriate encoding for a model family with caching."""
        encoding_name = TokenManager.MODEL_ENCODINGS.get(model_family)
        if not encoding_name:
            return None
            
        try:
            return tiktoken.encoding_for_model(encoding_name)
        except Exception as e:
            logger.warning(f"Failed to get encoding for {model_family}: {e}")
            return None
    
    @staticmethod
    def _get_model_family(model_name: str) -> str:
        """Determine the model family from model name."""
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
    @lru_cache(maxsize=256)
    def _cached_count(text_hash: str, model_family: str) -> int:
        """Cached token counting to avoid repeated calculations for the same text."""
        # This is a placeholder that will be filled with the real counting logic
        # Since we can't cache the actual text (might be too large), we use its hash
        pass
        
    @staticmethod
    def count_tokens(text: str, model_name: str) -> int:
        """Count tokens in text for a specific model with caching."""
        if not text:
            return 0
            
        # For very small texts, don't bother with caching
        if len(text) < 50:
            return TokenManager._count_tokens_impl(text, model_name)
            
        # For larger texts, use caching
        model_family = TokenManager._get_model_family(model_name)
        text_hash = hashlib.md5(text.encode()).hexdigest()
        
        # Try to get from cache
        try:
            # We can't use the actual function due to how lru_cache works,
            # so we'll implement a simple manual cache
            cache_key = f"{text_hash}:{model_family}"
            
            # Check if we have this in our static variable cache
            if not hasattr(TokenManager, "_token_count_cache"):
                TokenManager._token_count_cache = {}
                
            if cache_key in TokenManager._token_count_cache:
                return TokenManager._token_count_cache[cache_key]
                
            # Not in cache, calculate
            count = TokenManager._count_tokens_impl(text, model_name)
            
            # Store in cache (limit cache size)
            if len(TokenManager._token_count_cache) > 1000:
                # Simple cache eviction - clear half the cache
                keys = list(TokenManager._token_count_cache.keys())
                for k in keys[:500]:
                    del TokenManager._token_count_cache[k]
                    
            TokenManager._token_count_cache[cache_key] = count
            return count
        except Exception as e:
            logger.error(f"Error in token counting cache: {e}")
            # Fallback to direct calculation
            return TokenManager._count_tokens_impl(text, model_name)
    
    @staticmethod
    def _count_tokens_impl(text: str, model_name: str) -> int:
        """Actual token counting implementation."""
        model_family = TokenManager._get_model_family(model_name)
        encoding = TokenManager._get_encoding(model_family)
        
        if encoding:
            try:
                return len(encoding.encode(text))
            except Exception as e:
                logger.warning(f"Error encoding with tiktoken: {e}")
                # Fall back to approximation
                
        # Fallback approximation for when tiktoken fails or isn't available
        words = len(text.split())
        chars = len(text)
        return words + int(chars / 4)
        
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