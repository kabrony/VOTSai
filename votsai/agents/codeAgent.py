#!/usr/bin/env python3
"""
A simple plugin-based code agent that can generate and fix code across multiple programming languages.
"""

from abc import ABC, abstractmethod


# Define the plugin interface
class CodePlugin(ABC):
    @abstractmethod
    def generate_code(self, description: str) -> str:
        """Generate code based on a description."""
        pass

    @abstractmethod
    def fix_code(self, code: str) -> str:
        """Fix or lint a given snippet of code."""
        pass


# Example plugin for Python
class PythonPlugin(CodePlugin):
    def generate_code(self, description: str) -> str:
        # In a real-world scenario, integrate with an AI model (e.g., GPT-4) for code generation
        return f"# Python code generated for: {description}\nprint('Hello, world!')"

    def fix_code(self, code: str) -> str:
        # Simple fix: Correct a common typo in printing (e.g., 'prin(' to 'print(')
        fixed_code = code.replace("prin(", "print(")
        return fixed_code


# Example plugin for Go
class GoPlugin(CodePlugin):
    def generate_code(self, description: str) -> str:
        return (f"// Go code generated for: {description}\n"
                "package main\n\n"
                "import \"fmt\"\n\n"
                "func main() {\n\tfmt.Println(\"Hello, Go\")\n}\n")

    def fix_code(self, code: str) -> str:
        # For demonstration, no modifications are made
        return code


# Main agent that manages and uses plugins
class CodeAgent:
    def __init__(self):
        self.plugins = {}

    def register_plugin(self, language: str, plugin: CodePlugin):
        self.plugins[language.lower()] = plugin

    def generate(self, language: str, description: str) -> str:
        plugin = self.plugins.get(language.lower())
        if plugin:
            return plugin.generate_code(description)
        else:
            return f"Language '{language}' not supported."

    def fix(self, language: str, code: str) -> str:
        plugin = self.plugins.get(language.lower())
        if plugin:
            return plugin.fix_code(code)
        else:
            return f"Language '{language}' not supported."


# Example usage
if __name__ == "__main__":
    agent = CodeAgent()
    agent.register_plugin("python", PythonPlugin())
    agent.register_plugin("go", GoPlugin())

    # Generate Python code
    description = "A simple greeting program in Python"
    print("Generated Python Code:")
    print(agent.generate("python", description))

    print("\nFixed Python Code Example:")
    # Example with a bug (typo in print statement)
    broken_python_code = "prin('Hello, world!')"
    print("Before fixing:")
    print(broken_python_code)
    print("After fixing:")
    print(agent.fix("python", broken_python_code))

    # Generate Go code
    print("\nGenerated Go Code:")
    print(agent.generate("go", "A basic Go program for greeting")) 