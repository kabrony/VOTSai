"""
Router Module

Analyzes queries and determines the optimal model for processing.
"""
import logging
from typing import Dict, Any, List, Optional
import re

logger = logging.getLogger(__name__)

class Router:
    """
    Router for analyzing queries and selecting appropriate models
    
    This class:
    - Analyzes query characteristics
    - Selects the optimal model based on query type
    - Tracks model performance for continuous improvement
    """
    
    def __init__(self):
        """Initialize the router"""
        self.performance_history = {}
        logger.info("Router initialized")
        
    def analyze(self, query: str) -> Dict[str, Any]:
        """
        Analyze a query to determine its characteristics
        
        Args:
            query: The user query
            
        Returns:
            Dictionary with query analysis
        """
        analysis = {
            "length": len(query),
            "complexity": self._estimate_complexity(query),
            "domain": self._identify_domain(query),
            "requires_external_info": self._needs_external_info(query),
            "is_code_related": self._is_code_related(query)
        }
        
        logger.debug(f"Query analysis: {analysis}")
        return analysis
        
    def route(self, 
             query: str,
             analysis: Dict[str, Any],
             available_models: List[str],
             context: Optional[Dict[str, Any]] = None) -> str:
        """
        Select the optimal model for a query
        
        Args:
            query: The user query
            analysis: Query analysis from the analyze method
            available_models: List of available model names
            context: Additional context
            
        Returns:
            Name of the selected model
        """
        if not available_models:
            logger.warning("No models available for routing")
            return "none"
            
        # Default to first model if only one is available
        if len(available_models) == 1:
            return available_models[0]
            
        # Score each model based on the query characteristics
        scores = {}
        for model_name in available_models:
            scores[model_name] = self._score_model_for_query(model_name, analysis)
            
        # Get the model with the highest score
        best_model = max(scores.items(), key=lambda x: x[1])[0]
        logger.info(f"Selected model: {best_model} for query domain: {analysis['domain']}")
        
        return best_model
        
    def _estimate_complexity(self, query: str) -> float:
        """
        Estimate the complexity of a query (0.0-1.0)
        
        Args:
            query: The user query
            
        Returns:
            Complexity score
        """
        # Simple heuristic based on query length and structure
        length_factor = min(1.0, len(query) / 500)  # Longer queries are more complex
        
        # Check for complex question patterns
        complex_patterns = [
            r"why", r"how", r"explain", r"compare", r"difference",
            r"analyze", r"relationship between", r"impact of"
        ]
        
        pattern_matches = sum(1 for pattern in complex_patterns if re.search(pattern, query.lower()))
        pattern_factor = min(1.0, pattern_matches / len(complex_patterns))
        
        # Count the number of distinct "thought points"
        sentences = re.split(r'[.!?]', query)
        sentence_factor = min(1.0, len(sentences) / 10)
        
        # Combine factors
        complexity = 0.4 * length_factor + 0.4 * pattern_factor + 0.2 * sentence_factor
        return min(1.0, complexity)
        
    def _identify_domain(self, query: str) -> str:
        """
        Identify the knowledge domain of a query
        
        Args:
            query: The user query
            
        Returns:
            Domain identifier
        """
        # Simple keyword matching for domains
        query_lower = query.lower()
        
        # Define domain patterns
        domains = {
            "coding": [
                r"code", r"program", r"function", r"class", r"python",
                r"javascript", r"java", r"library", r"api", r"algorithm"
            ],
            "math": [
                r"math", r"calculate", r"formula", r"equation", r"solve",
                r"derivative", r"integral", r"algorithm", r"statistics"
            ],
            "science": [
                r"physics", r"chemistry", r"biology", r"science",
                r"experiment", r"theory", r"hypothesis", r"scientific"
            ],
            "history": [
                r"history", r"war", r"century", r"ancient", r"medieval",
                r"revolution", r"empire", r"civilization", r"historical"
            ],
            "philosophy": [
                r"philosophy", r"ethics", r"moral", r"meaning", r"existence",
                r"consciousness", r"reality", r"truth", r"philosophical"
            ],
            "creative": [
                r"write", r"create", r"story", r"poem", r"creative",
                r"imagine", r"fiction", r"narrative", r"character"
            ]
        }
        
        # Score each domain
        domain_scores = {}
        for domain, patterns in domains.items():
            score = sum(1 for pattern in patterns if re.search(r'\b' + pattern + r'\b', query_lower))
            domain_scores[domain] = score
            
        # Find domain with highest score
        if any(domain_scores.values()):
            return max(domain_scores.items(), key=lambda x: x[1])[0]
            
        # Default domain if no clear match
        return "general"
        
    def _needs_external_info(self, query: str) -> bool:
        """
        Determine if a query likely needs external information
        
        Args:
            query: The user query
            
        Returns:
            True if external info is likely needed
        """
        query_lower = query.lower()
        
        # Patterns suggesting need for external info
        external_patterns = [
            r"latest", r"recent", r"current", r"today", r"news",
            r"website", r"online", r"update", r"trending"
        ]
        
        for pattern in external_patterns:
            if re.search(r'\b' + pattern + r'\b', query_lower):
                return True
                
        return False
        
    def _is_code_related(self, query: str) -> bool:
        """
        Determine if a query is related to code
        
        Args:
            query: The user query
            
        Returns:
            True if code-related
        """
        query_lower = query.lower()
        
        # Patterns suggesting code-related content
        code_patterns = [
            r"code", r"program", r"function", r"class", r"method",
            r"bug", r"error", r"syntax", r"library", r"framework",
            r"algorithm", r"data structure", r"compile", r"runtime"
        ]
        
        for pattern in code_patterns:
            if re.search(r'\b' + pattern + r'\b', query_lower):
                return True
                
        # Check for code blocks
        if re.search(r'```[a-z]*\n', query):
            return True
            
        return False
        
    def _score_model_for_query(self, model_name: str, analysis: Dict[str, Any]) -> float:
        """
        Score a model's suitability for a query
        
        Args:
            model_name: Name of the model to score
            analysis: Query analysis data
            
        Returns:
            Suitability score (0.0-1.0)
        """
        # Define model strengths by domain
        model_strengths = {
            # Ollama models
            "ollama_llama2": {
                "general": 0.7,
                "coding": 0.6,
                "math": 0.6,
                "science": 0.7,
                "history": 0.7,
                "philosophy": 0.7,
                "creative": 0.7
            },
            "ollama_codellama": {
                "general": 0.6,
                "coding": 0.9,
                "math": 0.7,
                "science": 0.6,
                "history": 0.5,
                "philosophy": 0.5,
                "creative": 0.5
            },
            # Claude models (updated names)
            "claude-3-opus-20240229": {
                "general": 0.95,
                "coding": 0.92,
                "math": 0.9,
                "science": 0.93,
                "history": 0.95,
                "philosophy": 0.97,
                "creative": 0.95
            },
            "claude-3-sonnet-20240229": {
                "general": 0.93,
                "coding": 0.9,
                "math": 0.88,
                "science": 0.91,
                "history": 0.93,
                "philosophy": 0.95,
                "creative": 0.94
            },
            # DeepSeek models
            "deepseek-coder": {
                "general": 0.7,
                "coding": 0.95,
                "math": 0.85,
                "science": 0.75,
                "history": 0.65,
                "philosophy": 0.6,
                "creative": 0.6
            },
            # Perplexity models
            "sonar-medium-online": {
                "general": 0.85,
                "coding": 0.75,
                "math": 0.8,
                "science": 0.9,
                "history": 0.9,
                "philosophy": 0.85,
                "creative": 0.8,
                "requires_external_info": 0.98  # Special handling for web search
            }
        }
        
        # Get domain
        domain = analysis["domain"]
        
        # Special case for models with web search capabilities
        if analysis["requires_external_info"] and "sonar" in model_name:
            return 0.95  # Strongly prefer Perplexity for web search queries
        
        # Get base score for the domain
        default_strength = 0.7
        model_domain_strength = model_strengths.get(model_name, {}).get(domain, default_strength)
        
        # Adjust for query complexity
        complexity = analysis["complexity"]
        complexity_adjustment = 0.0
        
        # More complex queries favor more capable models
        if model_name == "claude-3-opus-20240229":
            complexity_adjustment = 0.2 * complexity
        elif "llama" in model_name and complexity > 0.7:
            complexity_adjustment = -0.1 * complexity
            
        # Adjust for code-related queries
        if analysis["is_code_related"]:
            if "codellama" in model_name:
                complexity_adjustment += 0.15
            elif model_name == "claude-3-opus-20240229":
                complexity_adjustment += 0.1
                
        # Adjust for external info needs
        if analysis["requires_external_info"] and model_name == "claude-3-opus-20240229":
            complexity_adjustment += 0.15
            
        # Calculate final score
        score = model_domain_strength + complexity_adjustment
        
        # Ensure score is in valid range
        return max(0.0, min(1.0, score))
        
    def update_model_performance(self, model_name: str, domain: str, quality_score: float) -> None:
        """
        Update performance history for continuous improvement
        
        Args:
            model_name: The model used
            domain: The query domain
            quality_score: Quality score (0.0-1.0)
        """
        if model_name not in self.performance_history:
            self.performance_history[model_name] = {}
            
        if domain not in self.performance_history[model_name]:
            self.performance_history[model_name][domain] = []
            
        # Add the score
        self.performance_history[model_name][domain].append(quality_score)
        
        # Keep only the most recent 100 scores
        if len(self.performance_history[model_name][domain]) > 100:
            self.performance_history[model_name][domain] = self.performance_history[model_name][domain][-100:]
            
        logger.debug(f"Updated performance for {model_name} in {domain} domain: {quality_score:.2f}") 