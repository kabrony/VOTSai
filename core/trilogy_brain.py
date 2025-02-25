import asyncio
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class TrilogyBrain:
    """Central oracle/architect for the VOTSai AGI system"""
    
    def __init__(self, router, model_manager, memory_system, tools, evaluator):
        self.router = router
        self.model_manager = model_manager
        self.memory = memory_system
        self.tools = tools
        self.evaluator = evaluator
        logger.info("TRILOGY Brain initialized with all components")
    
    async def process_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Main entry point for processing a query through the TRILOGY Brain system
        """
        if context is None:
            context = {}
        
        # Start tracking execution
        start_time = asyncio.get_event_loop().time()
        execution_id = f"exec_{start_time}_{hash(query) % 10000}"
        logger.info(f"[{execution_id}] Processing query: {query[:50]}...")
        
        try:
            # Check if we have a strategy override in context
            if "strategy" in context:
                strategy = context["strategy"]
                logger.info(f"[{execution_id}] Using strategy override: {strategy}")
            else:
                # 1. Analyze query and determine execution strategy
                analysis = await self.router.analyze(query)
                
                # Apply thinking depth if specified
                if "thinking_depth" in context:
                    analysis["complexity"] = max(analysis["complexity"], context["thinking_depth"])
                    
                logger.info(f"[{execution_id}] Query analysis: {analysis}")
                
                # 2. Retrieve relevant memories
                memories = self.memory.retrieve_relevant(query, limit=5)
                logger.info(f"[{execution_id}] Retrieved {len(memories)} relevant memories")
                
                # 3. Plan execution based on analysis
                strategy = self.plan_execution(analysis)
                logger.info(f"[{execution_id}] Execution strategy: {strategy}")
            
            # 4. Execute primary model
            primary_result = await self.execute_primary_model(
                strategy, query, context.get("memories", []), context
            )
            logger.info(f"[{execution_id}] Primary model execution complete")
            
            # 5. Check if verification is needed
            if strategy.get("verification", False) and not context.get("skip_verification", False):
                verification_result = await self.execute_verification(
                    strategy, query, primary_result, context.get("memories", [])
                )
                logger.info(f"[{execution_id}] Verification complete")
                
                # 6. Synthesize results if verification was performed
                final_result = self.synthesize_results(primary_result, verification_result)
                logger.info(f"[{execution_id}] Results synthesized")
            else:
                final_result = primary_result
            
            # 7. Evaluate the quality of the result
            quality_score = self.evaluator.assess(query, final_result)
            logger.info(f"[{execution_id}] Quality assessment: {quality_score}")
            
            # 8. Update memory with the interaction (unless disabled)
            if not context.get("skip_memory", False):
                self.memory.add(query, final_result)
            
            # 9. Update router with performance data
            self.router.update_performance(strategy, quality_score)
            
            # Add metadata to result
            execution_time = asyncio.get_event_loop().time() - start_time
            final_result["metadata"] = {
                "execution_id": execution_id,
                "execution_time": execution_time,
                "quality_score": quality_score,
                "strategy": strategy
            }
            
            return final_result
            
        except Exception as e:
            logger.error(f"[{execution_id}] Error processing query: {str(e)}", exc_info=True)
            return {
                "answer": f"Error in TRILOGY Brain: {str(e)}",
                "metadata": {
                    "execution_id": execution_id,
                    "error": str(e),
                    "execution_time": asyncio.get_event_loop().time() - start_time
                }
            }
    
    def plan_execution(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Define the execution strategy based on query analysis"""
        # Default strategy
        strategy = {
            "primary_model": "Claude API",
            "backup_model": "DeepSeek API",
            "tools": [],
            "verification": False
        }
        
        # Adjust based on intent
        if analysis.get("intent") == "coding":
            strategy["primary_model"] = "DeepSeek API"
            strategy["backup_model"] = "Claude API"
            strategy["tools"] = ["code_executor"]
            
        elif analysis.get("intent") == "factual" or analysis.get("requires_recent_info", False):
            strategy["primary_model"] = "Perplexity API"
            strategy["backup_model"] = "Claude API"
            strategy["tools"] = ["web_search"]
            
        # Enable verification for complex queries
        if analysis.get("complexity", 0) > 0.7:
            strategy["verification"] = True
        
        return strategy
    
    async def execute_primary_model(self, strategy, query, memories, context):
        """Execute the primary model according to the strategy"""
        model_name = strategy.get("primary_model")
        tools = self.prepare_tools(strategy.get("tools", []))
        
        # Get model from model manager
        model = self.model_manager.get_model(model_name)
        
        # Format memories for the model
        memory_context = self.format_memories(memories)
        
        # Execute the model
        result = await model.query(
            query=query, 
            memory_context=memory_context,
            tools=tools,
            context=context
        )
        
        return result
    
    async def execute_verification(self, strategy, query, primary_result, memories):
        """Execute verification using backup model"""
        model_name = strategy.get("backup_model")
        model = self.model_manager.get_model(model_name)
        
        # Construct verification prompt
        verification_query = self.construct_verification_prompt(query, primary_result)
        
        # Execute backup model
        result = await model.query(
            query=verification_query,
            memory_context=self.format_memories(memories)
        )
        
        return result
    
    def synthesize_results(self, primary_result, verification_result):
        """Synthesize primary and verification results"""
        # For now, simply use the Claude API to synthesize
        # This could be enhanced later with a more sophisticated approach
        
        # Extract answers
        primary_answer = primary_result.get("answer", "")
        verification_answer = verification_result.get("answer", "")
        
        # If verification largely agrees with primary, use primary
        if self.evaluator.calculate_agreement(primary_answer, verification_answer) > 0.8:
            return primary_result
        
        # If significant disagreement, combine with explanations
        combined_answer = f"""
Primary analysis: {primary_answer}

Verification analysis: {verification_answer}

Synthesis: Based on the analyses above, the most accurate response is:
{self.select_best_parts(primary_answer, verification_answer)}
        """
        
        result = primary_result.copy()
        result["answer"] = combined_answer
        result["synthesized"] = True
        
        return result
    
    def prepare_tools(self, tool_names):
        """Prepare the specified tools for use"""
        prepared_tools = []
        for name in tool_names:
            tool = self.tools.get_tool(name)
            if tool:
                prepared_tools.append(tool)
        return prepared_tools
    
    def format_memories(self, memories):
        """Format memories for inclusion in model context"""
        if not memories:
            return ""
            
        formatted = "Previous relevant interactions:\n\n"
        for i, memory in enumerate(memories, 1):
            formatted += f"{i}. Q: {memory['query']}\n   A: {memory['response']}\n\n"
            
        return formatted
    
    def construct_verification_prompt(self, query, primary_result):
        """Construct a prompt for the verification model"""
        verification_prompt = f"""
I need you to verify the following response to a user query.

User Query: {query}

Response to verify: {primary_result.get('answer', '')}

Please analyze this response and evaluate:
1. Factual accuracy
2. Completeness of the answer
3. Any potential errors or misleading information

Then provide your own response to the original query, being sure to correct any issues you identified.
"""
        return verification_prompt
    
    def select_best_parts(self, primary, verification):
        """Select the best parts from both responses"""
        # This is a placeholder for more sophisticated selection logic
        # In a real implementation, this might use an LLM to synthesize
        combined = "After analyzing both responses:\n\n"
        
        # Find agreements and disagreements
        # For now, this is simplified
        combined += f"- {primary[:200]}...\n\n"
        combined += f"- Additionally: {verification[:200]}...\n\n"
        
        return combined 