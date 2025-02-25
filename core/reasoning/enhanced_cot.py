"""
Enhanced Chain of Thought Processor

Provides advanced reasoning capabilities with research integration.
"""
import logging
from typing import Dict, Any, List, Optional, Tuple
from core.reasoning.cot_processor import CoTProcessor

logger = logging.getLogger(__name__)

class EnhancedCoTProcessor(CoTProcessor):
    """
    Enhanced Chain of Thought processor with research capabilities
    
    Extends the base CoT processor with:
    - Web research integration
    - Multi-step reasoning
    - Source tracking
    """
    
    def __init__(self, max_depth: int = 5):
        """
        Initialize the enhanced CoT processor
        
        Args:
            max_depth: Maximum reasoning depth
        """
        super().__init__()
        self.max_depth = max_depth
        self.research_plugin = None
        logger.info("Enhanced CoT processor initialized")
    
    def register_research_plugin(self, plugin):
        """
        Register a research plugin
        
        Args:
            plugin: Research plugin to use
        """
        self.research_plugin = plugin
        logger.info(f"Registered research plugin: {plugin.name}")
    
    def process_with_research(self, 
                             query: str, 
                             model_fn,
                             thinking_depth: float = 0.7) -> Dict[str, Any]:
        """
        Process query with research steps
        
        Args:
            query: User query
            model_fn: Function to call the AI model
            thinking_depth: Depth of thinking (0.0-1.0)
            
        Returns:
            Processed result with reasoning steps and research
        """
        # Check if research plugin is available
        if not self.research_plugin:
            logger.warning("No research plugin available, falling back to standard CoT")
            return super().process(query, model_fn, thinking_depth)
        
        # Identify research topics based on the query
        research_topics = self._identify_research_topics(query, model_fn)
        
        # Conduct research if topics identified
        research_results = {}
        if research_topics:
            for topic in research_topics:
                # Execute search via research plugin
                search_result = self.research_plugin.execute("search", query=topic["query"])
                
                # If search successful and has results, browse top result
                if search_result.get("success") and search_result.get("results"):
                    top_result = search_result["results"][0]
                    browse_result = self.research_plugin.execute("browse", url=top_result["url"])
                    
                    # Store research results
                    research_results[topic["query"]] = {
                        "search": search_result,
                        "content": browse_result
                    }
        
        # Enhanced reasoning with research included
        reasoning_prompt = self._construct_research_prompt(query, research_results)
        
        # Generate reasoning with research incorporated
        reasoning_steps, final_answer = self._execute_reasoning_with_research(
            reasoning_prompt, 
            model_fn, 
            thinking_depth,
            research_results
        )
        
        # Format the response
        return {
            "query": query,
            "reasoning_steps": reasoning_steps,
            "answer": final_answer,
            "research": {
                "topics": research_topics,
                "results": research_results
            }
        }
    
    def _identify_research_topics(self, 
                                query: str, 
                                model_fn) -> List[Dict[str, Any]]:
        """
        Identify research topics for a query
        
        Args:
            query: User query
            model_fn: Function to call the AI model
            
        Returns:
            List of research topics
        """
        # Construct prompt to identify research needs
        research_prompt = f"""
        I need to answer the following question:
        
        {query}
        
        To provide an accurate and comprehensive answer, I need to identify specific topics that require research. 
        Please identify 1-3 specific search queries that would help gather relevant information.
        
        For each topic, provide:
        1. The specific search query to use
        2. Why this information is needed to answer the question
        
        Format as JSON:
        [
            {{
                "query": "specific search query",
                "reason": "why this information is needed"
            }}
        ]
        """
        
        # Get model's analysis
        response = model_fn(research_prompt)
        
        # Extract JSON (handling potential formatting issues)
        try:
            import re
            import json
            
            # Find anything that looks like a JSON array
            json_match = re.search(r'\[\s*\{.*\}\s*\]', response, re.DOTALL)
            
            if json_match:
                research_topics = json.loads(json_match.group(0))
                logger.info(f"Identified {len(research_topics)} research topics")
                return research_topics
            else:
                logger.warning("Could not parse research topics, using fallback method")
                # Fallback: Extract queries directly using regex
                queries = re.findall(r'query":\s*"([^"]+)"', response)
                return [{"query": q, "reason": "Direct information needed"} for q in queries]
                
        except Exception as e:
            logger.error(f"Error parsing research topics: {e}")
            # Ultimate fallback: Use the original query
            return [{"query": query, "reason": "Direct information needed"}]
    
    def _construct_research_prompt(self, 
                                  query: str, 
                                  research_results: Dict[str, Any]) -> str:
        """
        Construct prompt with research results
        
        Args:
            query: User query
            research_results: Research results
            
        Returns:
            Prompt including research
        """
        prompt = f"""
        I need to answer the following question:
        
        {query}
        
        I've gathered the following research to help answer this question:
        """
        
        # Add research results to prompt
        for topic, result in research_results.items():
            content = result.get("content", {})
            
            prompt += f"""
            
            RESEARCH TOPIC: {topic}
            
            SOURCE: {content.get("url", "Unknown source")}
            TITLE: {content.get("title", "Unknown title")}
            
            CONTENT:
            {content.get("content", "No content available")[:1000]}
            """
        
        prompt += """
        
        Based on this research, I'll think through this step-by-step:
        1. 
        """
        
        return prompt
    
    def _execute_reasoning_with_research(self, 
                                        prompt: str, 
                                        model_fn, 
                                        thinking_depth: float,
                                        research_results: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], str]:
        """
        Execute reasoning with research incorporated
        
        Args:
            prompt: Reasoning prompt with research
            model_fn: Function to call the AI model
            thinking_depth: Depth of thinking
            research_results: Research results
            
        Returns:
            Reasoning steps and final answer
        """
        # Determine number of reasoning steps based on thinking depth
        num_steps = max(2, int(self.max_depth * thinking_depth))
        
        reasoning_steps = []
        current_prompt = prompt
        
        # Generate reasoning steps
        for i in range(num_steps):
            # Get model's reasoning
            step_content = model_fn(current_prompt)
            
            # Extract step content
            if i < num_steps - 1:  # For all but the last step
                reasoning_steps.append({
                    "step": i + 1,
                    "content": step_content,
                    "sources": self._extract_sources(step_content, research_results)
                })
                
                # Update prompt for next step
                current_prompt = current_prompt + "\n" + step_content + f"\n{i+2}. "
            else:
                # Last step should include the final answer
                reasoning_steps.append({
                    "step": i + 1,
                    "content": step_content,
                    "sources": self._extract_sources(step_content, research_results)
                })
                
                # Extract final answer
                final_answer = self._extract_final_answer(step_content)
        
        return reasoning_steps, final_answer
    
    def _extract_sources(self, 
                        text: str, 
                        research_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract sources referenced in reasoning
        
        Args:
            text: Reasoning text
            research_results: Research results
            
        Returns:
            List of referenced sources
        """
        sources = []
        
        # Check each research result to see if it's referenced
        for topic, result in research_results.items():
            content = result.get("content", {})
            url = content.get("url", "")
            title = content.get("title", "")
            
            # Check if this source is referenced (simple check)
            if topic.lower() in text.lower() or title.lower() in text.lower() or url in text:
                sources.append({
                    "topic": topic,
                    "url": url,
                    "title": title
                })
        
        return sources
    
    def _extract_final_answer(self, text: str) -> str:
        """
        Extract final answer from reasoning
        
        Args:
            text: Reasoning text
            
        Returns:
            Final answer
        """
        # Look for specific markers that might indicate a final answer
        import re
        
        # Try different patterns
        patterns = [
            r"(?:Final Answer|In conclusion|To summarize|Therefore):?\s*(.+)$",
            r"(?:Answer|Conclusion|Summary):?\s*(.+)$"
        ]
        
        for pattern in patterns:
            matches = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if matches:
                return matches.group(1).strip()
        
        # If no specific marker found, return the last paragraph
        paragraphs = text.split("\n\n")
        return paragraphs[-1].strip() 