"""
Plugin Manager Module

Manages discovery, loading, and execution of plugins for TRILOGY Brain.
"""
import logging
import os
import sys
import importlib
import pkgutil
import inspect
from typing import Dict, Any, List, Optional, Type, Set, Tuple
import json

from core.plugins.base import PluginInterface, ToolPlugin, ContentPlugin, IntegrationPlugin

logger = logging.getLogger(__name__)

class PluginManager:
    """
    Manages the plugin ecosystem for TRILOGY Brain
    
    Provides:
    - Plugin discovery and loading
    - Plugin execution and management
    - Plugin configuration
    """
    
    def __init__(self, plugins_dir: str = "plugins"):
        """
        Initialize the plugin manager
        
        Args:
            plugins_dir: Directory to look for plugins
        """
        self.plugins_dir = plugins_dir
        self.registered_plugins: Dict[str, Type[PluginInterface]] = {}
        self.active_plugins: Dict[str, PluginInterface] = {}
        self.disabled_plugins: Set[str] = set()
        self.plugin_configs: Dict[str, Dict[str, Any]] = {}
        
        # Load plugin configurations
        self._load_plugin_configs()
        
        logger.info(f"Plugin manager initialized with plugins directory: {plugins_dir}")
    
    def discover_plugins(self) -> List[Tuple[str, Type[PluginInterface]]]:
        """
        Discover available plugins in the plugins directory
        
        Returns:
            List of tuples with plugin name and class
        """
        discovered = []
        
        # Ensure the plugins directory exists
        if not os.path.exists(self.plugins_dir):
            logger.warning(f"Plugins directory does not exist: {self.plugins_dir}")
            return discovered
        
        # Add plugins directory to path if not already there
        if self.plugins_dir not in sys.path:
            sys.path.insert(0, os.path.abspath(self.plugins_dir))
        
        # Discover plugin modules
        plugin_packages = [name for _, name, ispkg in pkgutil.iter_modules([self.plugins_dir]) if ispkg]
        
        for package_name in plugin_packages:
            try:
                # Import the plugin package
                package = importlib.import_module(package_name)
                
                # Find plugin classes in the package
                for _, obj in inspect.getmembers(package, inspect.isclass):
                    # Check if it's a plugin class (not imported from elsewhere)
                    if (inspect.getmodule(obj).__name__.startswith(package_name) and 
                        issubclass(obj, PluginInterface) and 
                        obj is not PluginInterface and
                        obj is not ToolPlugin and
                        obj is not ContentPlugin and
                        obj is not IntegrationPlugin):
                        
                        plugin_name = f"{package_name}.{obj.__name__}"
                        discovered.append((plugin_name, obj))
                        logger.debug(f"Discovered plugin: {plugin_name}")
                        
            except Exception as e:
                logger.error(f"Error discovering plugins in package {package_name}: {e}")
        
        return discovered
    
    def register_plugins(self) -> int:
        """
        Register available plugins
        
        Returns:
            Number of registered plugins
        """
        discovered = self.discover_plugins()
        
        # Register each discovered plugin
        for plugin_name, plugin_class in discovered:
            self.registered_plugins[plugin_name] = plugin_class
            logger.info(f"Registered plugin: {plugin_name}")
        
        return len(self.registered_plugins)
    
    def activate_plugin(self, plugin_name: str, **kwargs) -> bool:
        """
        Activate a registered plugin
        
        Args:
            plugin_name: Name of the plugin to activate
            kwargs: Additional parameters for plugin initialization
            
        Returns:
            Success status
        """
        if plugin_name in self.disabled_plugins:
            logger.warning(f"Plugin is disabled: {plugin_name}")
            return False
            
        if plugin_name in self.active_plugins:
            logger.debug(f"Plugin already active: {plugin_name}")
            return True
            
        if plugin_name not in self.registered_plugins:
            logger.warning(f"Plugin not registered: {plugin_name}")
            return False
        
        try:
            # Get plugin configuration
            config = self.plugin_configs.get(plugin_name, {})
            
            # Combine config with kwargs, with kwargs taking precedence
            init_params = {**config, **kwargs}
            
            # Instantiate the plugin
            plugin_instance = self.registered_plugins[plugin_name]()
            
            # Initialize the plugin
            if plugin_instance.initialize(**init_params):
                self.active_plugins[plugin_name] = plugin_instance
                logger.info(f"Activated plugin: {plugin_name}")
                return True
            else:
                logger.warning(f"Failed to initialize plugin: {plugin_name}")
                return False
        except Exception as e:
            logger.error(f"Error activating plugin {plugin_name}: {e}")
            return False
    
    def deactivate_plugin(self, plugin_name: str) -> bool:
        """
        Deactivate an active plugin
        
        Args:
            plugin_name: Name of the plugin to deactivate
            
        Returns:
            Success status
        """
        if plugin_name not in self.active_plugins:
            logger.warning(f"Plugin not active: {plugin_name}")
            return False
            
        try:
            # Call cleanup method
            self.active_plugins[plugin_name].cleanup()
            
            # Remove from active plugins
            del self.active_plugins[plugin_name]
            
            logger.info(f"Deactivated plugin: {plugin_name}")
            return True
        except Exception as e:
            logger.error(f"Error deactivating plugin {plugin_name}: {e}")
            return False
    
    def execute_plugin(self, plugin_name: str, command: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a command on an active plugin
        
        Args:
            plugin_name: Name of the plugin
            command: Command to execute
            kwargs: Additional parameters
            
        Returns:
            Result of the command
        """
        if plugin_name not in self.active_plugins:
            # Try to activate the plugin if it's registered
            if plugin_name in self.registered_plugins:
                if not self.activate_plugin(plugin_name):
                    return {"error": f"Plugin {plugin_name} could not be activated"}
            else:
                return {"error": f"Plugin {plugin_name} not found"}
        
        try:
            # Execute the command
            result = self.active_plugins[plugin_name].execute(command, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Error executing plugin {plugin_name} command {command}: {e}")
            return {"error": str(e)}
    
    def get_plugin_info(self, plugin_name: str) -> Dict[str, Any]:
        """
        Get information about a plugin
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            Plugin information
        """
        # Check active plugins first
        if plugin_name in self.active_plugins:
            plugin = self.active_plugins[plugin_name]
            return {
                "name": plugin.name,
                "description": plugin.description,
                "version": plugin.version,
                "capabilities": plugin.capabilities,
                "type": plugin.plugin_type,
                "status": "active"
            }
            
        # Then check registered plugins
        if plugin_name in self.registered_plugins:
            plugin_class = self.registered_plugins[plugin_name]
            
            # Create a temporary instance just to get properties
            try:
                temp_instance = plugin_class()
                return {
                    "name": temp_instance.name,
                    "description": temp_instance.description,
                    "version": temp_instance.version,
                    "capabilities": temp_instance.capabilities,
                    "type": getattr(temp_instance, "plugin_type", "unknown"),
                    "status": "registered"
                }
            except Exception as e:
                return {
                    "name": plugin_name,
                    "error": str(e),
                    "status": "error"
                }
        
        return {"name": plugin_name, "status": "not_found"}
    
    def list_plugins(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        List all plugins with their status
        
        Returns:
            Dictionary with active and registered plugins
        """
        active = []
        for name in sorted(self.active_plugins.keys()):
            active.append(self.get_plugin_info(name))
            
        registered = []
        for name in sorted(self.registered_plugins.keys()):
            if name not in self.active_plugins:
                registered.append(self.get_plugin_info(name))
        
        return {
            "active": active,
            "registered": registered
        }
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """
        Get all available tools from tool plugins
        
        Returns:
            List of available tools
        """
        tools = []
        
        for name, plugin in self.active_plugins.items():
            if isinstance(plugin, ToolPlugin):
                for command in plugin.tool_commands:
                    tools.append({
                        "name": f"{plugin.name}.{command}",
                        "description": plugin.get_tool_description(command),
                        "plugin": name,
                        "command": command
                    })
        
        return tools
    
    def _load_plugin_configs(self) -> None:
        """Load plugin configurations from file"""
        config_path = os.path.join("config", "plugins.json")
        
        try:
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    data = json.load(f)
                    
                    # Load configurations
                    self.plugin_configs = data.get("configs", {})
                    
                    # Load disabled plugins
                    self.disabled_plugins = set(data.get("disabled", []))
                    
                    logger.info(f"Loaded plugin configurations for {len(self.plugin_configs)} plugins")
            else:
                logger.debug(f"Plugin configuration file not found: {config_path}")
        except Exception as e:
            logger.error(f"Error loading plugin configurations: {e}")
    
    def _save_plugin_configs(self) -> None:
        """Save plugin configurations to file"""
        config_path = os.path.join("config", "plugins.json")
        
        try:
            # Ensure the config directory exists
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            # Prepare data
            data = {
                "configs": self.plugin_configs,
                "disabled": list(self.disabled_plugins)
            }
            
            # Save to file
            with open(config_path, "w") as f:
                json.dump(data, f, indent=2)
                
            logger.debug("Saved plugin configurations")
        except Exception as e:
            logger.error(f"Error saving plugin configurations: {e}")
    
    def set_plugin_config(self, plugin_name: str, config: Dict[str, Any]) -> None:
        """
        Set configuration for a plugin
        
        Args:
            plugin_name: Name of the plugin
            config: Configuration parameters
        """
        self.plugin_configs[plugin_name] = config
        self._save_plugin_configs()
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """
        Disable a plugin
        
        Args:
            plugin_name: Name of the plugin to disable
            
        Returns:
            Success status
        """
        # Deactivate if active
        if plugin_name in self.active_plugins:
            self.deactivate_plugin(plugin_name)
            
        # Add to disabled plugins
        self.disabled_plugins.add(plugin_name)
        self._save_plugin_configs()
        
        logger.info(f"Disabled plugin: {plugin_name}")
        return True
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """
        Enable a previously disabled plugin
        
        Args:
            plugin_name: Name of the plugin to enable
            
        Returns:
            Success status
        """
        if plugin_name in self.disabled_plugins:
            self.disabled_plugins.remove(plugin_name)
            self._save_plugin_configs()
            
            logger.info(f"Enabled plugin: {plugin_name}")
            return True
        
        return False 