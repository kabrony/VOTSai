import logging
from typing import Dict, Any
import difflib

logger = logging.getLogger(__name__)

class Evaluator:
    """Evaluation system for assessing response quality"""
    
    def __init__(self):
        # Metrics weights
        self.metrics = {
            "relevance": 0.3,
            "completeness": 0.3,
            "coherence": 0.2,
            "factuality": 0.2
        }
        
        logger.info("Evaluator initialized")
    
    def assess(self, query: str, result: Dict[str, Any]) -> float:
        """
        Assess the quality of a response
        Returns a score between 0.0 and 1.0
        """
        # Extract the answer text
        answer = result.get("answer", "")
        
        # Calculate individual metrics
        relevance = self.calculate_relevance(query, answer)
        completeness = self.calculate_completeness(query, answer)
        coherence = self.calculate_coherence(answer)
        factuality = self.calculate_factuality(answer)
        
        # Combine metrics using weights
        score = (
            relevance * self.metrics["relevance"] +
            completeness * self.metrics["completeness"] +
            coherence * self.metrics["coherence"] +
            factuality * self.metrics["factuality"]
        )
        
        # Ensure score is between 0 and 1
        score = min(max(score, 0.0), 1.0)
        
        logger.info(f"Evaluation score: {score:.2f} (R:{relevance:.2f}, C:{completeness:.2f}, Co:{coherence:.2f}, F:{factuality:.2f})")
        
        return score
    
    def calculate_relevance(self, query: str, answer: str) -> float:
        """
        Calculate how relevant the answer is to the query
        This is a placeholder - in a real system, this would use more sophisticated techniques
        """
        # Basic keyword matching
        query_words = set(query.lower().split())
        answer_words = set(answer.lower().split())
        
        # Calculate overlap
        common_words = query_words.intersection(answer_words)
        
        if len(query_words) == 0:
            return 0.0
            
        # Simple relevance score based on overlap
        return min(len(common_words) / len(query_words) * 1.5, 1.0)
    
    def calculate_completeness(self, query: str, answer: str) -> float:
        """
        Calculate how complete the answer is
        This is a placeholder - in a real system, this would use ML models
        """
        # Very simple heuristic based on answer length relative to query
        query_length = len(query.split())
        answer_length = len(answer.split())
        
        # Too short answers are incomplete
        if answer_length < query_length / 2:
            return 0.3
        
        # Very long answers are likely complete
        if answer_length > query_length * 3:
            return 0.9
            
        # Linear scaling in between
        return 0.5 + (answer_length - (query_length / 2)) / (query_length * 3 - query_length / 2) * 0.4
    
    def calculate_coherence(self, answer: str) -> float:
        """
        Calculate how coherent the answer is
        This is a placeholder - in a real system, this would use NLP models
        """
        # Simple heuristic based on sentence count and length
        sentences = answer.split('.')
        
        # Filter out empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) == 0:
            return 0.0
            
        # Very simple coherence metric
        words_per_sentence = sum(len(s.split()) for s in sentences) / len(sentences)
        
        # Too short or too long sentences might indicate poor coherence
        if words_per_sentence < 3:
            return 0.4
        elif words_per_sentence > 30:
            return 0.6
            
        # Optimal range is around 10-20 words per sentence
        return 0.7 + min(abs(words_per_sentence - 15), 5) / 5 * 0.3
    
    def calculate_factuality(self, answer: str) -> float:
        """
        Calculate likelihood of factual accuracy
        This is a placeholder - in a real system, this would use fact verification
        """
        # Without a true fact verification system, return a default value
        # Future enhancements could use external sources or a dedicated verification model
        return 0.8
    
    def calculate_agreement(self, text1: str, text2: str) -> float:
        """
        Calculate agreement between two texts
        Returns a score between 0.0 (complete disagreement) and 1.0 (complete agreement)
        """
        # Use difflib for string similarity as a basic measure of agreement
        similarity = difflib.SequenceMatcher(None, text1, text2).ratio()
        
        # Scale the similarity to account for paraphrasing
        # Even different wordings of the same content should have similarity > 0.2
        scaled_agreement = 0.5 + similarity / 2
        
        return scaled_agreement 