"""
Omega Platform Modules Package
All platform features are implemented as modules
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseModule(ABC):
    """Base class for all Omega modules"""
    
    def __init__(self, config: Dict[str, Any], engine):
        self.config = config
        self.engine = engine
        self.name = self.__class__.__name__.replace("Module", "").lower()
        self.running = False
    
    @abstractmethod
    def start(self):
        """Start the module"""
        pass
    
    @abstractmethod
    def stop(self):
        """Stop the module"""
        pass
    
    def status(self) -> Dict[str, Any]:
        """Get module status"""
        return {
            "name": self.name,
            "running": self.running,
            "config": self.config,
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check"""
        return {
            "healthy": self.running,
            "message": "Module is running" if self.running else "Module is stopped",
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        }
