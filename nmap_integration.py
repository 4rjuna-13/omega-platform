"""
Nmap Integration for Project Omega
Distributed, intelligent port scanning
"""
import subprocess
import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional
import asyncio

class OmegaNmapScanner:
    """Intelligent Nmap scanning with distributed capabilities"""
    
    def __init__(self):
        self.safety_mode = True
        self.allowed_targets = ["scanme.nmap.org", "192.168.1.1"]  # Safe targets
        
    async def intelligent_scan(self, target: str, scan_type: str = "basic") -> Dict:
        """Perform intelligent scanning based on target and context"""
        
        # Safety checks
        if self.safety_mode and target not in self.allowed_targets:
            return {
                "status": "blocked",
                "reason": "Safety mode enabled. Use allowed targets only.",
                "allowed_targets": self.allowed_targets
            }
        
        # Different scan types
        scan_commands = {
            "basic": f"nmap -sV -O {target}",
            "quick": f"nmap -F {target}",
            "stealth": f"nmap -sS {target}",
            "full": f"nmap -A -T4 {target}"
        }
        
        cmd = scan_commands.get(scan_type, scan_commands["basic"])
        
        try:
            # Run nmap scan
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                results = self._parse_nmap_output(stdout.decode())
                return {
                    "status": "success",
                    "target": target,
                    "scan_type": scan_type,
                    "results": results
                }
            else:
                return {
                    "status": "error",
                    "target": target,
                    "error": stderr.decode()
                }
                
        except Exception as e:
            return {
                "status": "exception",
                "target": target,
                "error": str(e)
            }
    
    def _parse_nmap_output(self, output: str) -> Dict:
        """Parse Nmap output into structured data"""
        lines = output.split('\n')
        ports = []
        current_port = None
        
        for line in lines:
            if '/tcp' in line or '/udp' in line:
                # Parse port line like "22/tcp open  ssh"
                parts = line.split()
                if len(parts) >= 3:
                    port_proto = parts[0]
                    state = parts[1]
                    service = parts[2] if len(parts) > 2 else "unknown"
                    
                    ports.append({
                        "port": port_proto,
                        "state": state,
                        "service": service
                    })
        
        # Extract OS detection if present
        os_info = "Unknown"
        for line in lines:
            if "OS details:" in line:
                os_info = line.split("OS details:")[1].strip()
            elif "Running:" in line:
                os_info = line.split("Running:")[1].strip()
        
        return {
            "open_ports": ports,
            "os_detection": os_info,
            "scan_timestamp": "Simulated - Implement actual parsing"
        }
    
    async def distributed_scan(self, targets: List[str]) -> Dict:
        """Perform distributed scanning across multiple nodes"""
        tasks = [self.intelligent_scan(target, "quick") for target in targets[:3]]  # Limit for safety
        results = await asyncio.gather(*tasks)
        
        return {
            "operation": "distributed_scan",
            "target_count": len(targets),
            "results": results,
            "note": "Limited to 3 targets in safety mode"
        }

# Test function
async def test_nmap_integration():
    """Test Nmap integration"""
    print("🔍 Testing Nmap Integration...")
    
    scanner = OmegaNmapScanner()
    
    # Test basic scan
    print("📡 Scanning safe target...")
    result = await scanner.intelligent_scan("scanme.nmap.org", "basic")
    
    print(f"Status: {result['status']}")
    print(f"Target: {result['target']}")
    
    if result['status'] == 'success':
        print(f"Found {len(result['results']['open_ports'])} open ports")
        for port in result['results']['open_ports'][:5]:  # Show first 5
            print(f"  • {port['port']}: {port['service']} ({port['state']})")
    
    print("✅ Nmap integration test complete")

if __name__ == "__main__":
    asyncio.run(test_nmap_integration())
