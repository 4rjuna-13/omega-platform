#!/usr/bin/env python3
"""
Simple Mobile Optimizer - Quick test version
"""
import os
import platform

class SimpleMobileOptimizer:
    def __init__(self):
        self.device_info = self.detect_device()
    
    def detect_device(self):
        """Simple device detection"""
        info = {
            "platform": platform.system(),
            "machine": platform.machine(),
            "is_termux": 'ANDROID_ROOT' in os.environ or 'TERMUX_VERSION' in os.environ,
            "is_linux": platform.system() == 'Linux'
        }
        return info
    
    def get_optimization(self):
        """Get optimization recommendations"""
        if self.device_info["is_termux"]:
            return {
                "level": "aggressive",
                "max_threads": 2,
                "memory_limit_mb": 256,
                "battery_saver": True
            }
        else:
            return {
                "level": "normal",
                "max_threads": 8,
                "memory_limit_mb": 2048,
                "battery_saver": False
            }

# Quick test
if __name__ == "__main__":
    print("🔍 Simple Mobile Optimizer Test")
    print("=" * 40)
    
    optimizer = SimpleMobileOptimizer()
    
    print(f"Platform: {optimizer.device_info['platform']}")
    print(f"Architecture: {optimizer.device_info['machine']}")
    print(f"Is Termux: {optimizer.device_info['is_termux']}")
    
    optimization = optimizer.get_optimization()
    print(f"\nOptimization Level: {optimization['level']}")
    print(f"Max Threads: {optimization['max_threads']}")
    print(f"Memory Limit: {optimization['memory_limit_mb']} MB")
    print(f"Battery Saver: {optimization['battery_saver']}")
