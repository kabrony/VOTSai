"""
Chain of Thought (CoT) Processor

Implements advanced reasoning capabilities based on Google Research's
chain of thought prompting techniques.
"""
import logging
import re
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger(__name__)

class CoTProcessor:
    """
    Processes prompts and responses to implement Chain of Thought reasoning.
    
    This processor:
    1. Enhances prompts with CoT examples
    2. Extracts reasoning steps from model responses
    3. Provides utilities for analyzing and improving reasoning paths
    """
    
    def __init__(self, 
                cot_temperature: float = 0.7,
                max_reasoning_steps: int = 10,
                extract_reasoning: bool = True,
                reasoning_format: str = "markdown"):
        """
        Initialize the CoT processor
        
        Args:
            cot_temperature: Temperature for CoT generation (higher = more exploratory reasoning)
            max_reasoning_steps: Maximum number of reasoning steps to generate/extract
            extract_reasoning: Whether to extract reasoning steps from responses
            reasoning_format: Format for displaying reasoning ("markdown" or "plain")
        """
        self.cot_temperature = cot_temperature
        self.max_reasoning_steps = max_reasoning_steps
        self.extract_reasoning = extract_reasoning
        self.reasoning_format = reasoning_format
        self.reasoning_templates = self._load_reasoning_templates()
        
        logger.info("Chain of Thought processor initialized")
    
    def _load_reasoning_templates(self) -> Dict[str, str]:
        """Load reasoning templates for different domains"""
        return {
            "general": "Let me think about this step by step:\n1. ",
            "math": "To solve this math problem, I'll work through it step by step:\n1. ",
            "code": "Let me analyze this code step by step:\n1. ",
            "science": "To answer this scientific question, I'll reason step by step:\n1. ",
            "logic": "Let me solve this logical problem systematically:\n1. "
        }
    
    def enhance_prompt(self, 
                     prompt: str, 
                     domain: str = "general",
                     system_prompt: Optional[str] = None) -> Tuple[str, str]:
        """
        Enhance a prompt with CoT instructions
        
        Args:
            prompt: Original user prompt
            domain: Reasoning domain (general, math, code, etc.)
            system_prompt: Optional system prompt to enhance
            
        Returns:
            Enhanced prompt and system prompt tuple
        """
        # Get appropriate reasoning template for domain
        template = self.reasoning_templates.get(domain, self.reasoning_templates["general"])
        
        # Don't modify prompt if it's short or already seems to request reasoning
        if len(prompt) < 20 or "step by step" in prompt.lower() or "explain your reasoning" in prompt.lower():
            return prompt, system_prompt or ""
        
        # Determine if this is a complex question deserving CoT
        complexity_indicators = [
            "why", "how", "explain", "analyze", "compare", "solve", "calculate",
            "predict", "what would happen", "reason", "evaluate"
        ]
        
        is_complex = any(indicator in prompt.lower() for indicator in complexity_indicators)
        
        if not is_complex:
            return prompt, system_prompt or ""
        
        # Enhance system prompt if provided
        enhanced_system_prompt = system_prompt or ""
        if system_prompt:
            if "reasoning" not in system_prompt.lower() and "step by step" not in system_prompt.lower():
                cot_instruction = "\nUse chain of thought reasoning to break down complex problems into steps. Show your reasoning process before providing the final answer."
                enhanced_system_prompt = system_prompt + cot_instruction
        else:
            enhanced_system_prompt = "You are an AI assistant that uses chain of thought reasoning to solve complex problems. Break down your thinking into clear steps before giving a final answer."
        
        return prompt, enhanced_system_prompt
    
    def extract_reasoning_steps(self, response: str) -> Tuple[List[str], str]:
        """
        Extract reasoning steps from model response
        
        Args:
            response: Model response text
            
        Returns:
            List of reasoning steps and final answer
        """
        # Check if response has numbered steps
        step_pattern = re.compile(r'(?:^|\n)(\d+)[.)\]]\s*(.*?)(?=(?:\n\d+[.)\]]|\n\n|$))', re.DOTALL)
        steps_match = step_pattern.findall(response)
        
        if steps_match:
            steps = [step[1].strip() for step in steps_match]
            
            # Try to find final answer after steps
            final_answer = ""
            final_patterns = [
                r'\n\s*(?:Therefore|Thus|In conclusion|So,|Finally|The answer is|To summarize),?\s*(.*?)(?:\n|$)',
                r'\n\s*(?:Answer|Result|Solution):?\s*(.*?)(?:\n|$)',
                r'\n\s*(?:Therefore|Thus|In conclusion|So|The final answer),?\s*(.*?)(?:\n|$)'
            ]
            
            for pattern in final_patterns:
                match = re.search(pattern, response, re.IGNORECASE)
                if match:
                    final_answer = match.group(1).strip()
                    break
            
            if not final_answer and len(response.split("\n\n")) > 1:
                # If no explicit conclusion marker, try last paragraph
                paragraphs = response.split("\n\n")
                final_answer = paragraphs[-1].strip()
            
            return steps, final_answer
        
        # Alternative: Look for reasoning markers
        reasoning_markers = [
            "First,", "Second,", "Third,", "Next,", "Then,", "Finally,", "Lastly,"
        ]
        
        if any(marker in response for marker in reasoning_markers):
            # Split by reasoning markers
            steps = []
            remaining_text = response
            
            for marker in reasoning_markers:
                if marker in remaining_text:
                    parts = remaining_text.split(marker, 1)
                    if len(parts) == 2 and parts[0].strip():
                        steps.append(parts[0].strip())
                    remaining_text = marker + parts[-1] if len(parts) == 2 else parts[0]
            
            if remaining_text.strip():
                steps.append(remaining_text.strip())
            
            final_answer = steps[-1] if steps else response
            steps = steps[:-1] if steps else []
            
            return steps, final_answer
        
        # If no structured reasoning found, return whole response as final answer
        return [], response
    
    def format_reasoning(self, steps: List[str], final_answer: str) -> str:
        """
        Format reasoning steps and final answer
        
        Args:
            steps: List of reasoning steps
            final_answer: Final answer text
            
        Returns:
            Formatted reasoning text
        """
        if not steps:
            return final_answer
            
        if self.reasoning_format == "markdown":
            formatted_steps = "\n".join([f"**Step {i+1}:** {step}" for i, step in enumerate(steps)])
            return f"{formatted_steps}\n\n**Final Answer:** {final_answer}"
        else:
            formatted_steps = "\n".join([f"Step {i+1}: {step}" for i, step in enumerate(steps)])
            return f"{formatted_steps}\n\nFinal Answer: {final_answer}"
    
    def process_response(self, response: str) -> Tuple[str, str, List[str]]:
        """
        Process a model response to extract and format reasoning
        
        Args:
            response: Model response text
            
        Returns:
            Tuple of (final answer, formatted reasoning, reasoning steps)
        """
        if not self.extract_reasoning:
            return response, "", []
            
        steps, final_answer = self.extract_reasoning_steps(response)
        formatted_reasoning = self.format_reasoning(steps, final_answer)
        
        # If no structured reasoning found, return original response
        if not steps:
            return response, "", []
            
        return final_answer, formatted_reasoning, steps 