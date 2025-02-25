import logging
from typing import Dict, Any, List
import numpy as np

logger = logging.getLogger(__name__)

class Router:
    """Advanced routing module for directing queries to appropriate models and tools"""
    
    def __init__(self, classifier, embedding_model):
        self.classifier = classifier
        self.embedding_model = embedding_model
        self.performance_history = {}
        logger.info("Router initialized")
    
    async def analyze(self, query: str) -> Dict[str, Any]:
        """
        Analyze a query to determine its characteristics
        """
        # Get the intent classification
        intent = self.classifier.classify(query)
        
        # Get query complexity score (0-1)
        complexity = self.calculate_complexity(query)
        
        # Determine if query requires recent information
        requires_recent = self.requires_recent_info(query)
        
        # Embed the query for later use
        embedding = self.embedding_model.embed(query)
        
        # Additional analysis can be added here
        
        return {
            "intent": intent,
            "complexity": complexity,
            "requires_recent_info": requires_recent,
            "embedding": embedding
        }
    
    def calculate_complexity(self, query: str) -> float:
        """
        Calculate the complexity of a query (0-1 scale)
        """
        # For now, use a simple heuristic based on length and structure
        # This can be replaced with a more sophisticated model later
        
        # Basic factors that might indicate complexity
        factors = [
            len(query) / 500,  # Length (normalize to 0-1 range, assuming 500 chars is complex)
            query.count("?") / 3,  # Number of questions (normalize)
            len(query.split()) / 100,  # Word count (normalize)
            sum(1 for c in query if c in "{}[]()") / 20  # Code-like characters
        ]
        
        # Cap each factor at 1.0
        factors = [min(f, 1.0) for f in factors]
        
        # Simple weighted average
        weights = [0.3, 0.2, 0.3, 0.2]
        complexity = sum(f * w for f, w in zip(factors, weights))
        
        return min(max(complexity, 0.0), 1.0)  # Ensure result is between 0 and 1
    
    def requires_recent_info(self, query: str) -> bool:
        """
        Determine if query likely requires recent information
        """
        # Check for keywords suggesting need for recent info
        recency_keywords = [
            "latest", "recent", "current", "today", "yesterday", 
            "this week", "this month", "this year", "news",
            "update", "newest", "trending"
        ]
        
        # Add website indicators
        website_indicators = [
            ".com", ".io", ".org", ".net", "website", "site",
            "webpage", "domain", "url", "online platform"
        ]
        
        query_lower = query.lower()
        
        # Check for recency keywords
        for keyword in recency_keywords:
            if keyword in query_lower:
                return True
                
        # Check for website indicators
        for indicator in website_indicators:
            if indicator in query_lower:
                return True
                
        return False
    
    def update_performance(self, strategy: Dict[str, Any], quality_score: float) -> None:
        """
        Update performance history for models based on execution results
        """
        model = strategy.get("primary_model")
        intent = strategy.get("intent", "general")
        
        if model not in self.performance_history:
            self.performance_history[model] = {}
            
        if intent not in self.performance_history[model]:
            self.performance_history[model][intent] = {
                "scores": [],
                "avg_score": 0.0
            }
            
        # Add new score
        self.performance_history[model][intent]["scores"].append(quality_score)
        
        # Update average (using last 50 scores at most)
        recent_scores = self.performance_history[model][intent]["scores"][-50:]
        self.performance_history[model][intent]["avg_score"] = sum(recent_scores) / len(recent_scores)
        
        logger.info(f"Updated performance history for {model} on {intent}: {quality_score:.2f}") 