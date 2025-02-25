"""
TRILOGY Brain Core

The main orchestration system that manages model selection,
memory integration, and response generation.
"""
import logging
import time
from typing import Dict, Any, List, Optional, Tuple, Union
import os
from core.reasoning.cot_processor import CoTProcessor
from core.plugins.manager import PluginManager
from core.reasoning.enhanced_cot import EnhancedCoTProcessor

logger = logging.getLogger(__name__)

class TrilogyBrain:
    """
    Main orchestration engine for the TRILOGY Brain system
    
    This class coordinates:
    - Model selection and routing
    - Memory and context management
    - Response generation and processing
    - Telemetry and analytics
    """
    
    def __init__(self, 
                model_registry=None, 
                router=None, 
                memory_system=None,
                telemetry=None,
                cot_processor=None,
                analytics=None,
                plugin_manager=None):
        """
        Initialize the TRILOGY Brain system
        
        Args:
            model_registry: Registry of available models
            router: Router for selecting appropriate models
            memory_system: System for managing conversation memory
            telemetry: System for tracking usage and performance
            cot_processor: Chain of Thought processor for enhanced reasoning
            analytics: Analytics system for tracking model performance
            plugin_manager: Plugin manager for managing plugins
        """
        # Import components if not provided
        if model_registry is None:
            from models.registry import ModelRegistry
            model_registry = ModelRegistry()
            
        if router is None:
            from core.router import Router
            router = Router()
            
        if memory_system is None:
            from core.memory_system import MemorySystem
            memory_system = MemorySystem()
            
        if telemetry is None:
            from utils.telemetry import Telemetry
            telemetry = Telemetry()
            
        self.model_registry = model_registry
        self.router = router
        self.memory_system = memory_system
        self.telemetry = telemetry
        
        # Initialize CoT processor if not provided
        if cot_processor is None:
            self.cot_processor = CoTProcessor()
        else:
            self.cot_processor = cot_processor
        
        # Initialize analytics
        self.analytics = analytics
        
        # Initialize plugin manager
        if plugin_manager is None:
            self.plugin_manager = PluginManager()
            # Discover and register plugins
            self.plugin_manager.register_plugins()
        else:
            self.plugin_manager = plugin_manager
        
        self.default_model = "auto"  # Can be overridden by user
        logger.info("TRILOGY Brain system initialized with Chain of Thought and Plugin capabilities")
        
    def process_query(self, 
                     query: str, 
                     context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a user query through the TRILOGY Brain system with CoT reasoning
        
        Args:
            query: The user's input query
            context: Additional context for processing
            
        Returns:
            Dictionary containing the response and metadata
        """
        start_time = time.time()
        context = context or {}
        thinking_depth = context.get("thinking_depth", 0.5)
        
        # Track query in telemetry
        query_id = self.telemetry.track_query(query)
        
        # Analyze the query to determine domain
        analysis = self.router.analyze(query)
        domain = analysis["domain"]
        
        # Enhance with Chain of Thought prompting if enabled
        use_cot = context.get("use_cot", True)
        if use_cot:
            # Get system prompt
            system_prompt = self._get_system_prompt(thinking_depth)
            
            # Enhance with CoT
            query, system_prompt = self.cot_processor.enhance_prompt(
                query, 
                domain=domain,
                system_prompt=system_prompt
            )
            
            # Update context with enhanced system prompt
            if context is None:
                context = {}
            context["system_prompt"] = system_prompt
        
        # Get relevant memories
        memories = self.memory_system.get_relevant_memories(query)
        
        # Select model based on query analysis
        selected_model_name = self._select_model(query, context)
        logger.info(f"Selected model for query: {selected_model_name}")
        
        # Get the model instance
        try:
            model = self.model_registry.get_model(selected_model_name)
        except Exception as e:
            logger.error(f"Error getting model {selected_model_name}: {e}")
            # Fallback to another available model
            available_models = self.model_registry.list_available_models()
            if available_models:
                selected_model_name = available_models[0]
                model = self.model_registry.get_model(selected_model_name)
            else:
                return {
                    "answer": f"Error: No models available. {str(e)}",
                    "model": "none",
                    "metadata": {
                        "execution_time": time.time() - start_time,
                        "error": str(e)
                    }
                }
                
        # Prepare conversation context including memories
        conversation = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add memory context if available
        if memories:
            memory_text = "\n\n".join([f"Previous conversation: {m['text']}" for m in memories])
            conversation.append({
                "role": "system",
                "content": f"Relevant context from previous conversations:\n{memory_text}"
            })
            
        # Add the user query
        conversation.append({"role": "user", "content": query})
        
        # Generate response
        try:
            if hasattr(model, 'chat'):
                response = model.chat(conversation)
            else:
                # Fallback for models without chat interface
                combined_prompt = "\n\n".join([m["content"] for m in conversation])
                response = model.generate(combined_prompt)
                
            # Extract the answer and metadata
            answer = response.get("text", "")
            model_used = response.get("model", selected_model_name)
            metadata = response.get("metadata", {})
            thinking = response.get("thinking", "")
            
            # Add to memory
            self.memory_system.add_memory(query, answer)
            
            # Track in telemetry
            execution_time = time.time() - start_time
            self.telemetry.track_response(
                query_id=query_id,
                model=model_used,
                execution_time=execution_time,
                token_count=metadata.get("total_tokens", 0)
            )
            
            # Process result with CoT processor
            if use_cot and "answer" in response:
                final_answer, formatted_reasoning, reasoning_steps = self.cot_processor.process_response(response["answer"])
                
                # Include reasoning in result
                response["answer"] = final_answer
                response["thinking"] = formatted_reasoning
                response["reasoning_steps"] = reasoning_steps
            
            # Track the model usage for analytics
            usage_id = self.analytics.track_model_usage(
                model=model_used,
                domain=domain,
                query=query,
                execution_time=execution_time,
                token_count=metadata.get("total_tokens", 0),
                success=True  # Assume success if no exception
            )
            
            # Store usage_id in the response metadata for potential feedback
            metadata["usage_id"] = usage_id
            
            return {
                "answer": answer,
                "model": model_used,
                "thinking": thinking,
                "metadata": {
                    **metadata,
                    "execution_time": execution_time,
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            execution_time = time.time() - start_time
            self.telemetry.track_error(query_id, str(e))
            
            return {
                "answer": f"I encountered an error while processing your request: {str(e)}",
                "model": selected_model_name,
                "metadata": {
                    "execution_time": execution_time,
                    "error": str(e)
                }
            }
            
    def _select_model(self, query: str, context: Dict[str, Any]) -> str:
        """
        Select the appropriate model for a given query
        
        Args:
            query: The user query
            context: Additional context
            
        Returns:
            Name of the selected model
        """
        # Check for explicit model override
        if "model_override" in context and context["model_override"]:
            return context["model_override"]
            
        # Use the router to analyze and select model
        query_analysis = self.router.analyze(query)
        
        # Get available models
        available_models = self.model_registry.list_available_models()
        
        # Let the router decide
        return self.router.route(
            query=query,
            analysis=query_analysis,
            available_models=available_models,
            context=context
        )
        
    def _get_system_prompt(self, thinking_depth: float) -> str:
        """
        Generate a system prompt based on thinking depth
        
        Args:
            thinking_depth: Value between 0 and 1 indicating depth of reasoning
            
        Returns:
            System prompt text
        """
        base_prompt = """You are TRILOGY Brain, an advanced AI assistant that provides helpful, accurate, and thoughtful responses."""
        
        if thinking_depth > 0.7:
            return base_prompt + """
            Think step-by-step and show your detailed reasoning process in your answers.
            First break down complex problems into smaller parts.
            Explain your approach and assumptions clearly.
            Provide nuanced perspectives when appropriate.
            """
        elif thinking_depth > 0.3:
            return base_prompt + """
            Show your reasoning when answering complex questions.
            Be thorough but concise in your explanations.
            """
        else:
            return base_prompt + """
            Provide direct, concise answers to questions.
            """ 

    def execute_plugin(self, plugin_name: str, command: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a plugin command
        
        Args:
            plugin_name: Name of the plugin
            command: Command to execute
            kwargs: Additional parameters
            
        Returns:
            Result of the command
        """
        if self.plugin_manager:
            return self.plugin_manager.execute_plugin(plugin_name, command, **kwargs)
        else:
            return {"error": "Plugin system not available"}

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Get available tools from plugins
        
        Returns:
            List of available tools
        """
        if self.plugin_manager:
            return self.plugin_manager.get_tools()
        else:
            return []

    def list_plugins(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        List all plugins
        
        Returns:
            Dictionary with active and registered plugins
        """
        if self.plugin_manager:
            return self.plugin_manager.list_plugins()
        else:
            return {"active": [], "registered": []}

    def research_with_cot(self, 
                        query: str, 
                        context: Optional[Dict[str, Any]] = None,
                        thinking_depth: float = 0.7) -> Dict[str, Any]:
        """
        Process a query with chain of thought reasoning and web research
        
        Args:
            query: User query
            context: Optional context information
            thinking_depth: Depth of thinking (0.0-1.0)
            
        Returns:
            Response with reasoning and research
        """
        try:
            start_time = time.time()
            
            # Initialize enhanced CoT processor if needed
            if not hasattr(self, "enhanced_cot_processor"):
                self.enhanced_cot_processor = EnhancedCoTProcessor()
                
                # Register research plugin if available
                if hasattr(self, "plugin_manager"):
                    research_plugins = [
                        p for p in self.plugin_manager.active_plugins.values() 
                        if p.name == "WebResearch"
                    ]
                    if research_plugins:
                        self.enhanced_cot_processor.register_research_plugin(research_plugins[0])
            
            # Select model
            model_name = self.default_model
            if context and "model_override" in context:
                model_name = context["model_override"]
            
            # Get model instance
            model = self.model_registry.get_model(model_name)
            
            # Define model function for CoT to use
            def model_fn(prompt):
                return model.generate(prompt, max_tokens=2048).strip()
            
            # Process with enhanced CoT
            result = self.enhanced_cot_processor.process_with_research(
                query=query,
                model_fn=model_fn,
                thinking_depth=thinking_depth
            )
            
            # Calculate execution time
            execution_time = time.time() - start_time
            
            # Add metadata
            metadata = {
                "model": model_name,
                "execution_time": execution_time,
                "method": "research_with_cot",
                "thinking_depth": thinking_depth
            }
            
            # Track in memory system
            if self.memory_system:
                self.memory_system.add_memory(
                    query=query,
                    response=result["answer"],
                    metadata={
                        **metadata,
                        "reasoning_steps": result["reasoning_steps"],
                        "research": result["research"]
                    }
                )
            
            # Return result with metadata
            return {
                "query": query,
                "answer": result["answer"],
                "reasoning_steps": result["reasoning_steps"],
                "research": result["research"],
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Error in research_with_cot: {e}")
            return {
                "query": query,
                "answer": f"Error processing query with research: {str(e)}",
                "reasoning_steps": [],
                "research": {},
                "metadata": {"error": str(e)}
            } 