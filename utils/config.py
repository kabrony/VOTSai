import os
import yaml
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class Config:
    """Configuration manager for VOTSai."""
    
    _instance = None
    _config = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._load_config()
        return cls._instance
    
    @classmethod
    def _load_config(cls):
        """Load configuration from file and environment variables."""
        # Default configuration
        cls._config = {
            "app": {
                "name": "VOTSai",
                "version": "2.0.0",
                "log_level": "INFO",
            },
            "models": {
                "timeout": 60,
                "default": "Auto",
                "temperature": 0.7,
            },
            "memory": {
                "db_path": "vots_agi_memory.db",
                "short_term_max": 20,
            },
        }
        
        # Load from config file if exists
        config_path = os.environ.get("VOTSAI_CONFIG", "config.yaml")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    file_config = yaml.safe_load(f)
                    cls._update_nested_dict(cls._config, file_config)
                logger.info(f"Loaded configuration from {config_path}")
            except Exception as e:
                logger.error(f"Failed to load configuration from {config_path}: {e}")
                
        # Override with environment variables
        cls._load_from_env()
    
    @classmethod
    def _load_from_env(cls):
        """Load configuration from environment variables."""
        prefix = "VOTSAI_"
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower().replace("__", ".")
                cls.set(config_key, cls._convert_value(value))
    
    @staticmethod
    def _convert_value(value: str) -> Any:
        """Convert string value to appropriate type."""
        if value.lower() in ("true", "yes", "1", "on"):
            return True
        elif value.lower() in ("false", "no", "0", "off"):
            return False
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value
    
    @classmethod
    def _update_nested_dict(cls, d: Dict, u: Dict) -> Dict:
        """Update nested dictionary recursively."""
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                cls._update_nested_dict(d[k], v)
            else:
                d[k] = v
        return d
    
    @classmethod
    def reload(cls) -> None:
        """Reload configuration from file and environment variables."""
        cls._load_config()
        logger.info("Configuration reloaded")
    
    @classmethod
    def save_config(cls, config_path: str = "config.yaml") -> bool:
        """Save current configuration to file."""
        try:
            with open(config_path, "w") as f:
                yaml.dump(cls._config, f, default_flow_style=False)
            logger.info(f"Saved configuration to {config_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save configuration to {config_path}: {e}")
            return False
    
    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """Set configuration value."""
        keys = key.split(".")
        d = cls._config
        for k in keys[:-1]:
            if k not in d:
                d[k] = {}
            d = d[k]
        d[keys[-1]] = value
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        keys = key.split(".")
        d = cls._config
        for k in keys:
            if k not in d:
                return default
            d = d[k]
        return d 