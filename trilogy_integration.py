import os
import logging
import asyncio
import streamlit as st
from dotenv import load_dotenv

# Import the TRILOGY Brain components
from core.trilogy_brain import TrilogyBrain
from core.router import Router
from core.model_manager import ModelManager
from core.memory_system import MemorySystem
from core.evaluator import Evaluator
from core.tools import ToolModule

# Import the embedding model
from core.embeddings import EmbeddingModel

# Import the intent classifier
from core.classifier import IntentClassifier

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='trilogy_brain.log'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class TrilogyIntegration:
    """Integration class for the TRILOGY Brain with VOTSai"""
    
    def __init__(self):
        logger.info("Initializing TRILOGY Brain integration")
        
        # Initialize components
        self.embedding_model = EmbeddingModel()
        self.classifier = IntentClassifier()
        
        # Create router
        self.router = Router(self.classifier, self.embedding_model)
        
        # Create model manager
        self.model_manager = ModelManager()
        
        # Create memory system
        self.memory_system = MemorySystem(self.embedding_model)
        
        # Create tools module
        self.tools = ToolModule()
        
        # Create evaluator
        self.evaluator = Evaluator()
        
        # Create TRILOGY Brain
        self.trilogy_brain = TrilogyBrain(
            self.router,
            self.model_manager,
            self.memory_system,
            self.tools,
            self.evaluator
        )
        
        logger.info("TRILOGY Brain integration initialized successfully")
    
    async def process_query(self, query, context=None):
        """
        Process a query through the TRILOGY Brain
        
        Args:
            query: The user's query
            context: Optional context information like model_override, thinking_depth, etc.
        """
        if context is None:
            context = {}
        
        # Handle model override
        if "model_override" in context and context["model_override"] != "Auto":
            logger.info(f"Model override: {context['model_override']}")
            # Modify the context to include model override info
            context["strategy"] = {"primary_model": f"{context['model_override']} API"}
        
        # Handle thinking depth setting
        if "thinking_depth" in context:
            logger.info(f"Thinking depth set to: {context['thinking_depth']}")
            # This can be used to adjust complexity threshold in router
        
        # Process the query
        result = await self.trilogy_brain.process_query(query, context)
        
        # Add thinking information if available
        if "thinking" in context and context["thinking"]:
            # In a real system, you might extract thinking process from model responses
            # For now, we'll just create a stub thinking process
            result["thinking"] = f"TRILOGY Brain analyzed query complexity: {context.get('thinking_depth', 0.7)}\n" + \
                                f"Selected model: {result.get('model', 'Unknown')}\n" + \
                                f"Execution strategy: {result.get('metadata', {}).get('strategy', {})}"
        
        return result


# Initialize the integration
trilogy_integration = TrilogyIntegration()

async def process_query_async(query, context=None):
    """
    Asynchronous wrapper for processing queries
    """
    return await trilogy_integration.process_query(query, context)

def process_query(query, context=None):
    """
    Synchronous wrapper for processing queries (for Streamlit)
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(process_query_async(query, context))
    loop.close()
    return result 