#!/usr/bin/env python3
"""
Production Configuration Manager for JAIDA-Omega-SAIOS
"""

import yaml
import json
import os
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    """Manages production configuration"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.config = {}
            self.environment = os.getenv('ENVIRONMENT', 'development')
            self.config_path = Path('config')
            self.load_config()
            self.initialized = True
    
    def load_config(self):
        """Load configuration based on environment"""
        config_files = [
            self.config_path / 'base.yaml',
            self.config_path / f'{self.environment}.yaml',
            self.config_path / 'secrets.yaml'  # Git-ignored secrets file
        ]
        
        for config_file in config_files:
            if config_file.exists():
                print(f"📄 Loading config: {config_file}")
                with open(config_file, 'r') as f:
                    file_config = yaml.safe_load(f) or {}
                    self._deep_merge(self.config, file_config)
        
        # Override with environment variables
        self._apply_env_overrides()
        
        print(f"✅ Configuration loaded for {self.environment} environment")
    
    def _deep_merge(self, base: Dict, update: Dict):
        """Deep merge two dictionaries"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def _apply_env_overrides(self):
        """Apply environment variable overrides"""
        env_prefix = "JAIDA_"
        
        for env_key, env_value in os.environ.items():
            if env_key.startswith(env_prefix):
                config_key = env_key[len(env_prefix):].lower()
                keys = config_key.split('__')
                
                # Convert string values to appropriate types
                if env_value.lower() in ('true', 'false'):
                    env_value = env_value.lower() == 'true'
                elif env_value.isdigit():
                    env_value = int(env_value)
                elif self._is_float(env_value):
                    env_value = float(env_value)
                
                # Set nested config value
                current = self.config
                for key in keys[:-1]:
                    if key not in current:
                        current[key] = {}
                    current = current[key]
                current[keys[-1]] = env_value
    
    def _is_float(self, value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        current = self.config
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        
        return current
    
    def save_current_config(self):
        """Save current config for debugging"""
        debug_path = Path('logs/config_debug.json')
        debug_path.parent.mkdir(exist_ok=True)
        
        with open(debug_path, 'w') as f:
            json.dump(self.config, f, indent=2, default=str)
        
        print(f"📊 Config saved to {debug_path}")
    
    def validate(self):
        """Validate configuration"""
        required = [
            'database.path',
            'data_sources.siem.enabled',
            'alert_processing.severity_threshold'
        ]
        
        for req in required:
            if self.get(req) is None:
                raise ValueError(f"Missing required config: {req}")
        
        print("✅ Configuration validation passed")

# Global config instance
config = ConfigManager()

if __name__ == "__main__":
    print("🔧 Current Configuration:")
    print(json.dumps(config.config, indent=2, default=str))
    
    # Example usage
    db_path = config.get('database.path')
    print(f"\n📁 Database path: {db_path}")
    
    siem_enabled = config.get('data_sources.siem.enabled')
    print(f"📡 SIEM enabled: {siem_enabled}")
