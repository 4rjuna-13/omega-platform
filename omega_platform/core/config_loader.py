"""
Hierarchical configuration loader for Omega Platform
"""

import os
import yaml
import json
from typing import Dict, Any, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ConfigLoader:
    """Load configuration from multiple sources with precedence"""
    
    CONFIG_PATHS = [
        "/etc/omega-platform/",
        "~/.omega-platform/",
        "./config/",
    ]
    
    def __init__(self):
        self.config = {}
    
    def load(self, config_file: Optional[str] = None, env: str = "development") -> Dict[str, Any]:
        """
        Load configuration with hierarchy:
        1. Defaults (built-in)
        2. Config file (if specified)
        3. Environment-specific overrides
        4. Environment variables
        5. Command line overrides
        """
        
        # Step 1: Load defaults
        self.config = self._load_defaults()
        
        # Step 2: Load from config file if provided
        if config_file and os.path.exists(config_file):
            file_config = self._load_file(config_file)
            self._merge_configs(self.config, file_config)
        
        # Step 3: Load environment-specific config
        env_config = self._load_environment_config(env)
        self._merge_configs(self.config, env_config)
        
        # Step 4: Override with environment variables
        env_vars = self._load_environment_vars()
        self._merge_configs(self.config, env_vars)
        
        logger.info(f"Configuration loaded for environment: {env}")
        return self.config
    
    def _load_defaults(self) -> Dict[str, Any]:
        """Load default configuration"""
        return {
            "platform": {
                "name": "Omega Platform",
                "version": "3.0.0",
                "debug": False,
                "log_level": "INFO",
            },
            "modules": {
                "deception": {"enabled": True, "port": 8080},
                "prediction": {"enabled": True},
                "response": {"enabled": True},
                "simulation": {"enabled": False},
                "collaboration": {"enabled": False},
                "cloud": {"enabled": False},
                "ai_assistant": {"enabled": False},
            },
            "api": {
                "enabled": True,
                "host": "0.0.0.0",
                "port": 8000,
                "cors_origins": ["http://localhost:3000"],
            },
            "security": {
                "auth_required": False,
                "audit_logging": True,
                "encryption": {
                    "algorithm": "A256GCM",
                    "key_rotation_days": 30,
                }
            },
            "data": {
                "storage_path": "./data",
                "retention_days": 90,
                "backup_enabled": True,
            }
        }
    
    def _load_file(self, file_path: str) -> Dict[str, Any]:
        """Load configuration from file (YAML or JSON)"""
        try:
            with open(file_path, 'r') as f:
                if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                    return yaml.safe_load(f) or {}
                elif file_path.endswith('.json'):
                    return json.load(f) or {}
                else:
                    logger.warning(f"Unsupported config file format: {file_path}")
                    return {}
        except Exception as e:
            logger.error(f"Failed to load config file {file_path}: {e}")
            return {}
    
    def _load_environment_config(self, env: str) -> Dict[str, Any]:
        """Load environment-specific configuration"""
        env_file = f"config/environments/{env}.yaml"
        if os.path.exists(env_file):
            return self._load_file(env_file)
        return {}
    
    def _load_environment_vars(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        config = {}
        
        # Map environment variables to config structure
        env_mappings = {
            "OMEGA_LOG_LEVEL": ["platform", "log_level"],
            "OMEGA_DEBUG": ["platform", "debug"],
            "OMEGA_API_PORT": ["api", "port"],
            "OMEGA_API_HOST": ["api", "host"],
            "OMEGA_STORAGE_PATH": ["data", "storage_path"],
        }
        
        for env_var, config_path in env_mappings.items():
            if env_var in os.environ:
                self._set_nested(config, config_path, os.environ[env_var])
        
        return config
    
    def _merge_configs(self, base: Dict[str, Any], overlay: Dict[str, Any]):
        """Recursively merge two dictionaries"""
        for key, value in overlay.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_configs(base[key], value)
            else:
                base[key] = value
    
    def _set_nested(self, d: Dict[str, Any], path: list, value: Any):
        """Set a nested dictionary value using path list"""
        for key in path[:-1]:
            d = d.setdefault(key, {})
        d[path[-1]] = value

def load_config(config_file: Optional[str] = None, env: str = "development") -> Dict[str, Any]:
    """Convenience function to load configuration"""
    loader = ConfigLoader()
    return loader.load(config_file, env)
