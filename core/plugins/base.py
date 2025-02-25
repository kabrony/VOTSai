"""
Plugin Base Module

Defines the base classes and interfaces for TRILOGY Brain plugins.
"""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable, Type

logger = logging.getLogger(__name__)

class PluginInterface(ABC):
    """
    Base interface for all TRILOGY Brain plugins
    
    All plugins must implement this interface to be recognized by the system.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the plugin"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of the plugin's functionality"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Version of the plugin"""
        pass
    
    @property
    def capabilities(self) -> List[str]:
        """List of plugin capabilities"""
        return []
    
    @abstractmethod
    def initialize(self, **kwargs) -> bool:
        """
        Initialize the plugin with optional parameters
        
        Returns:
            Success status
        """
        pass
    
    @abstractmethod
    def execute(self, command: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a command with the plugin
        
        Args:
            command: Command to execute
            kwargs: Additional parameters
            
        Returns:
            Result of the command
        """
        pass
    
    def cleanup(self) -> None:
        """Perform cleanup when plugin is disabled"""
        pass


class ToolPlugin(PluginInterface):
    """
    Plugin that provides external tools for use in conversations
    
    Tool plugins extend the capabilities of the AI by allowing it
    to perform actions in the real world or access external systems.
    """
    
    @property
    def plugin_type(self) -> str:
        """Type of plugin"""
        return "tool"
    
    @property
    @abstractmethod
    def tool_commands(self) -> List[str]:
        """List of available tool commands"""
        pass
    
    @abstractmethod
    def get_tool_description(self, command: str) -> str:
        """
        Get description of a specific tool command
        
        Args:
            command: Tool command name
            
        Returns:
            Human-readable description
        """
        pass


class ContentPlugin(PluginInterface):
    """
    Plugin that modifies or enhances content
    
    Content plugins alter, enhance, or add content to the
    conversation, such as formatting, translation, etc.
    """
    
    @property
    def plugin_type(self) -> str:
        """Type of plugin"""
        return "content"
    
    @abstractmethod
    def process_input(self, text: str, **kwargs) -> str:
        """
        Process user input before sending to model
        
        Args:
            text: User input text
            kwargs: Additional parameters
            
        Returns:
            Processed text
        """
        pass
    
    @abstractmethod
    def process_output(self, text: str, **kwargs) -> str:
        """
        Process model output before sending to user
        
        Args:
            text: Model output text
            kwargs: Additional parameters
            
        Returns:
            Processed text
        """
        pass


class IntegrationPlugin(PluginInterface):
    """
    Plugin that integrates with external services
    
    Integration plugins connect TRILOGY Brain with external
    services, APIs, or systems for expanded functionality.
    """
    
    @property
    def plugin_type(self) -> str:
        """Type of plugin"""
        return "integration"
    
    @abstractmethod
    def authenticate(self, **credentials) -> bool:
        """
        Authenticate with the external service
        
        Args:
            credentials: Authentication credentials
            
        Returns:
            Authentication success
        """
        pass
    
    @abstractmethod
    def service_call(self, endpoint: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Make a call to the external service
        
        Args:
            endpoint: Service endpoint
            data: Request data
            kwargs: Additional parameters
            
        Returns:
            Service response
        """
        pass 