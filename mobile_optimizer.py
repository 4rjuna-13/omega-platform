"""
MOBILE OPTIMIZER - Android Termux Performance Engine
Ensures revolutionary performance on mobile devices
"""
import os
import psutil
import platform
from typing import Dict, Any
import asyncio

class MobileOptimizer:
    """Optimizes Omega for mobile/edge devices"""
    
    def __init__(self):
        self.device_info = self._detect_device()
        self.optimization_profile = self._create_optimization_profile()
        self.resource_limits = self._calculate_resource_limits()
        
    def _detect_device(self) -> Dict[str, Any]:
        """Detect device type and capabilities"""
        device_info = {
            "platform": platform.system(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "memory_total": psutil.virtual_memory().total // (1024*1024),  # MB
            "cpu_count": psutil.cpu_count(logical=False) or 1,
            "is_mobile": self._check_if_mobile(),
            "battery_saver": False,
            "thermal_throttling": False
        }
        
        # Android/Termux detection
        if 'ANDROID_ROOT' in os.environ:
            device_info["platform"] = "Android Termux"
            device_info["is_mobile"] = True
            device_info["optimization_level"] = "aggressive"
        
        # Raspberry Pi detection
        if 'raspberrypi' in platform.uname().release.lower():
            device_info["platform"] = "Raspberry Pi"
            device_info["is_arm"] = True
            device_info["optimization_level"] = "moderate"
        
        return device_info
    
    def _check_if_mobile(self) -> bool:
        """Check if running on mobile device"""
        mobile_indicators = [
            'ANDROID_ROOT' in os.environ,
            'ANDROID_DATA' in os.environ,
            platform.machine() in ['armv7l', 'aarch64', 'arm64'],
            'mobile' in platform.platform().lower(),
            'termux' in platform.platform().lower()
        ]
        return any(mobile_indicators)
    
    def _create_optimization_profile(self) -> Dict[str, Any]:
        """Create device-specific optimization profile"""
        if self.device_info["is_mobile"]:
            return {
                "max_threads": 2,
                "memory_limit_mb": min(512, self.device_info["memory_total"] // 2),
                "scan_timeout": 120,  # seconds
                "batch_size": 10,
                "use_compression": True,
                "cache_aggressively": True,
                "prioritize_battery": True,
                "network_quota_limit": 50,  # MB per operation
                "background_operations": False
            }
        else:
            return {
                "max_threads": 8,
                "memory_limit_mb": self.device_info["memory_total"] // 4,
                "scan_timeout": 300,
                "batch_size": 100,
                "use_compression": False,
                "cache_aggressively": False,
                "prioritize_battery": False,
                "network_quota_limit": None,
                "background_operations": True
            }
    
    def _calculate_resource_limits(self) -> Dict[str, Any]:
        """Calculate safe resource limits"""
        profile = self.optimization_profile
        
        return {
            "cpu_percent": 70 if self.device_info["is_mobile"] else 90,
            "memory_percent": 60 if self.device_info["is_mobile"] else 80,
            "disk_quota_mb": 100 if self.device_info["is_mobile"] else 1000,
            "network_rate_kbps": 512 if self.device_info["is_mobile"] else 10240,
            "max_concurrent_scans": 1 if self.device_info["is_mobile"] else 5,
            "thermal_threshold": 45 if self.device_info["is_mobile"] else 70
        }
    
    def optimize_scan_parameters(self, target: str, scan_type: str) -> Dict[str, Any]:
        """Optimize scan parameters for current device"""
        base_params = {
            "target": target,
            "scan_type": scan_type,
            "optimized_for": self.device_info["platform"]
        }
        
        if self.device_info["is_mobile"]:
            # Mobile-optimized scanning
            return {
                **base_params,
                "ports": "top-100",
                "timing": "T2",  # Polite timing
                "max_retries": 2,
                "parallel_tasks": 1,
                "service_detection": "light",
                "script_scanning": False,
                "os_detection": False,
                "traceroute": False,
                "battery_saver": True,
                "data_saver": True,
                "result_compression": True
            }
        else:
            # Full capability scanning
            return {
                **base_params,
                "ports": "1-65535",
                "timing": "T4",
                "max_retries": 5,
                "parallel_tasks": profile["max_threads"],
                "service_detection": "full",
                "script_scanning": True,
                "os_detection": True,
                "traceroute": True,
                "battery_saver": False,
                "data_saver": False,
                "result_compression": False
            }
    
    def check_resource_availability(self) -> Dict[str, bool]:
        """Check if resources are available for operation"""
        checks = {
            "memory_available": psutil.virtual_memory().available > self.optimization_profile["memory_limit_mb"] * 1024 * 1024,
            "cpu_available": psutil.cpu_percent(interval=0.1) < self.resource_limits["cpu_percent"],
            "disk_space": psutil.disk_usage('/').free > self.resource_limits["disk_quota_mb"] * 1024 * 1024,
            "battery_ok": self._check_battery_status(),
            "thermal_ok": self._check_temperature()
        }
        
        return {
            **checks,
            "can_proceed": all(checks.values()),
            "limiting_factor": [k for k, v in checks.items() if not v][0] if not all(checks.values()) else None
        }
    
    def _check_battery_status(self) -> bool:
        """Check battery status (mobile only)"""
        if not self.device_info["is_mobile"]:
            return True
        
        try:
            # Try to get battery info on Termux
            import subprocess
            result = subprocess.run(['termux-battery-status'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                import json
                battery = json.loads(result.stdout)
                percentage = battery.get('percentage', 100)
                charging = battery.get('status', 'DISCHARGING') == 'CHARGING'
                
                # Don't perform heavy operations if battery low and not charging
                if percentage < 20 and not charging:
                    return False
            return True
        except:
            # If we can't check battery, assume it's OK
            return True
    
    def _check_temperature(self) -> bool:
        """Check device temperature"""
        try:
            # Try to read temperature (works on some systems)
            import subprocess
            result = subprocess.run(['cat', '/sys/class/thermal/thermal_zone0/temp'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                temp_c = int(result.stdout.strip()) / 1000
                return temp_c < self.resource_limits["thermal_threshold"]
            return True
        except:
            return True
    
    async def adaptive_throttling(self, operation: str, progress_callback=None):
        """Dynamically throttle operations based on resources"""
        iteration = 0
        
        while True:
            resources = self.check_resource_availability()
            
            if not resources["can_proceed"]:
                # Apply backoff
                backoff_time = min(30, 2 ** iteration)  # Exponential backoff
                print(f"[THROTTLING] Resource constraint: {resources['limiting_factor']}. "
                      f"Backing off for {backoff_time}s")
                
                await asyncio.sleep(backoff_time)
                iteration += 1
            else:
                # Reset backoff on success
                iteration = 0
                break
            
            if progress_callback:
                progress_callback(resources)
    
    def get_optimization_report(self) -> Dict[str, Any]:
        """Generate optimization report"""
        return {
            "device_info": self.device_info,
            "optimization_profile": self.optimization_profile,
            "resource_limits": self.resource_limits,
            "current_resources": {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_free_gb": psutil.disk_usage('/').free // (1024**3)
            },
            "recommendations": self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate optimization recommendations"""
        recs = []
        
        if self.device_info["is_mobile"]:
            recs.extend([
                "Use Wi-Fi instead of mobile data for large scans",
                "Charge device during intensive operations",
                "Close other apps to free memory",
                "Schedule scans for off-peak hours",
                "Use 'light' scan modes for quick assessments"
            ])
        
        if psutil.virtual_memory().percent > 80:
            recs.append("Memory usage high - consider reducing scan scope")
        
        if psutil.cpu_percent() > 70:
            recs.append("CPU usage high - throttling recommended")
        
        return recs

# Quick test
if __name__ == "__main__":
    optimizer = MobileOptimizer()
    report = optimizer.get_optimization_report()
    
    print(f"Platform: {report['device_info']['platform']}")
    print(f"Memory: {report['device_info']['memory_total']} MB")
    print(f"Mobile Optimized: {report['device_info']['is_mobile']}")
    
    # Test scan optimization
    scan_params = optimizer.optimize_scan_parameters("example.com", "discovery")
    print(f"\nOptimized Scan Parameters:")
    for k, v in scan_params.items():
        print(f"  {k}: {v}")
