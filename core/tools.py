import logging
import subprocess
import requests
import asyncio
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ToolModule:
    """Module for external tools and utilities"""
    
    def __init__(self):
        # Initialize available tools
        self.tools = {
            "code_executor": CodeExecutor(),
            "web_search": WebSearch(),
            "calculator": Calculator()
        }
        
        logger.info(f"Tool module initialized with {len(self.tools)} tools")
    
    def get_tool(self, tool_name: str):
        """Get a tool by name"""
        if tool_name in self.tools:
            return self.tools[tool_name]
        else:
            logger.warning(f"Tool {tool_name} not found")
            return None
    
    def list_tools(self) -> List[str]:
        """List all available tools"""
        return list(self.tools.keys())

    def __iter__(self):
        """Make ToolModule iterable"""
        return iter(self.tools.items())


class CodeExecutor:
    """Tool for executing code"""
    
    def __init__(self):
        self.supported_languages = ["python", "javascript", "bash"]
        self.max_execution_time = 10  # seconds
    
    async def execute(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Execute code in a sandboxed environment
        """
        if language not in self.supported_languages:
            return {
                "success": False,
                "output": f"Language {language} not supported. Supported languages: {', '.join(self.supported_languages)}",
                "error": "UnsupportedLanguage"
            }
        
        logger.info(f"Executing {language} code: {code[:50]}...")
        
        if language == "python":
            return await self._execute_python(code)
        elif language == "javascript":
            return await self._execute_javascript(code)
        elif language == "bash":
            return await self._execute_bash(code)
    
    async def _execute_python(self, code: str) -> Dict[str, Any]:
        """Execute Python code"""
        # In a real system, this would use a secure sandbox
        try:
            # Create a temporary file
            with open("temp_code.py", "w") as f:
                f.write(code)
            
            # Execute the code with timeout
            process = await asyncio.create_subprocess_exec(
                "python", "temp_code.py",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), 
                    timeout=self.max_execution_time
                )
                
                return {
                    "success": process.returncode == 0,
                    "output": stdout.decode(),
                    "error": stderr.decode() if stderr else None
                }
            except asyncio.TimeoutError:
                process.kill()
                return {
                    "success": False,
                    "output": None,
                    "error": f"Execution timed out after {self.max_execution_time} seconds"
                }
                
        except Exception as e:
            return {
                "success": False,
                "output": None,
                "error": str(e)
            }
    
    async def _execute_javascript(self, code: str) -> Dict[str, Any]:
        """Execute JavaScript code using Node.js"""
        # Similar implementation to Python but using Node.js
        # This is a placeholder
        return {
            "success": False,
            "output": None,
            "error": "JavaScript execution not implemented yet"
        }
    
    async def _execute_bash(self, code: str) -> Dict[str, Any]:
        """Execute Bash code"""
        # Similar implementation to Python but using bash
        # This is a placeholder
        return {
            "success": False,
            "output": None,
            "error": "Bash execution not implemented yet"
        }


class WebSearch:
    """Tool for web search"""
    
    def __init__(self):
        self.search_api_key = None  # Would use an actual API key
    
    async def search(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Perform a web search
        """
        logger.info(f"Searching the web for: {query}")
        
        # In a real implementation, this would use a search API
        # This is a placeholder
        return {
            "success": True,
            "results": [
                {
                    "title": f"Sample result for {query}",
                    "snippet": f"This is a placeholder result for the query '{query}'",
                    "url": "https://example.com"
                }
            ]
        }


class Calculator:
    """Tool for math calculations"""
    
    def calculate(self, expression: str) -> Dict[str, Any]:
        """
        Evaluate a mathematical expression
        """
        logger.info(f"Calculating: {expression}")
        
        try:
            # Basic security: only allow certain characters
            allowed_chars = set("0123456789+-*/().^% ")
            if not all(c in allowed_chars for c in expression):
                return {
                    "success": False,
                    "result": None,
                    "error": "Expression contains disallowed characters"
                }
            
            # Replace ^ with ** for exponentiation
            expression = expression.replace("^", "**")
            
            # Evaluate the expression
            result = eval(expression)
            
            return {
                "success": True,
                "result": result,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "result": None,
                "error": str(e)
            } 