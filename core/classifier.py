import logging
import re

logger = logging.getLogger(__name__)

class IntentClassifier:
    """Simple intent classifier for query routing"""
    
    def __init__(self):
        # Define patterns for different intents
        self.patterns = {
            "coding": [
                r'\bcode\b', r'\bprogramming\b', r'\bfunction\b', 
                r'\bpython\b', r'\bjavascript\b', r'\bclass\b',
                r'\bapi\b', r'\bsql\b', r'\balgorithm\b'
            ],
            "factual": [
                r'\bwhat is\b', r'\bdefine\b', r'\bmeaning\b',
                r'\bwhen\b', r'\bwhere\b', r'\bwho\b', r'\bhow many\b'
            ],
            "conceptual": [
                r'\bexplain\b', r'\bwhy\b', r'\bhow does\b',
                r'\bconcept\b', r'\btheory\b', r'\bprinciple\b'
            ],
            "web_search": [
                r'\blatest\b', r'\bnews\b', r'\brecent\b',
                r'\btoday\b', r'\bcurrent\b', r'\bfind\b'
            ]
        }
        logger.info("Intent classifier initialized")
    
    def classify(self, query):
        """
        Classify the intent of a query
        Returns one of: coding, factual, conceptual, web_search, general
        """
        query = query.lower()
        
        # Check each intent pattern
        scores = {intent: 0 for intent in self.patterns}
        
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, query):
                    scores[intent] += 1
        
        # Find intent with highest score
        max_score = 0
        max_intent = "general"  # Default intent
        
        for intent, score in scores.items():
            if score > max_score:
                max_score = score
                max_intent = intent
        
        logger.info(f"Classified query as '{max_intent}' intent")
        return max_intent

    def train(self):
        """
        Placeholder for training method (required by app.py)
        """
        logger.info("Classifier training not needed for rule-based implementation")
        return True