"""
INTEGRATION SCRIPT FOR DECEPTION ENGINE
Patches the main Omega server to include deception capabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def integrate_deception_engine(omega_server):
    """Integrate deception engine into the main Omega server"""
    
    # Import deception modules
    from deception_engine import DeceptionEngine
    import deception_api
    
    # Create deception engine instance
    omega_server.deception_engine = DeceptionEngine(omega_server)
    
    # Setup API endpoints
    deception_api.setup_deception_api(omega_server.app, omega_server.deception_engine)
    
    # Add deception commands to command processor
    if hasattr(omega_server, 'command_processor'):
        original_process_command = omega_server.command_processor
        
        def enhanced_process_command(command):
            """Enhanced command processor with deception commands"""
            cmd_lower = command.lower()
            
            # Deception engine commands
            if cmd_lower.startswith("deception start"):
                level = "MEDIUM"
                if "paranoid" in cmd_lower:
                    level = "PARANOID"
                elif "high" in cmd_lower:
                    level = "HIGH"
                elif "low" in cmd_lower:
                    level = "LOW"
                
                result = omega_server.deception_engine.start_deception_mode(level)
                return f"Deception Engine started at {level} level. {result.get('message', '')}"
            
            elif cmd_lower.startswith("deception stop"):
                result = omega_server.deception_engine.stop_deception_mode()
                return f"Deception Engine stopped. {result.get('message', '')}"
            
            elif cmd_lower.startswith("deception status"):
                stats = omega_server.deception_engine.get_deception_stats()
                return f"Deception Status: Active={stats['active']}, Level={stats['level']}, Honeypots={stats['honeypots_active']}, Connections={stats['total_connections']}"
            
            elif cmd_lower.startswith("deploy honeypot"):
                # Extract honeypot type
                parts = command.split()
                if len(parts) >= 3:
                    honeypot_type = parts[2]
                    result = omega_server.deception_engine.deploy_honeypot(honeypot_type)
                    return f"Honeypot deployment: {result.get('message', 'Unknown result')}"
                else:
                    return "Usage: deploy honeypot [type] (types: fake_ssh, fake_web, fake_db, fake_ftp, fake_api)"
            
            # Pass through to original processor
            return original_process_command(command)
        
        omega_server.command_processor = enhanced_process_command
    
    # Add deception status to system metrics
    original_get_system_metrics = omega_server.get_system_metrics
    
    def enhanced_get_system_metrics():
        """Enhanced metrics with deception info"""
        metrics = original_get_system_metrics()
        
        # Add deception metrics
        if hasattr(omega_server, 'deception_engine'):
            deception_stats = omega_server.deception_engine.get_deception_stats()
            metrics['deception'] = {
                'active': deception_stats['active'],
                'level': deception_stats['level'],
                'honeypots': deception_stats['honeypots_active'],
                'connections': deception_stats['total_connections'],
                'attackers': deception_stats['unique_attackers']
            }
        
        return metrics
    
    omega_server.get_system_metrics = enhanced_get_system_metrics
    
    # Add deception to threat prediction
    if hasattr(omega_server, 'threat_predictor'):
        original_predict_threat = omega_server.threat_predictor.predict
        
        def enhanced_predict_threat(data):
            """Enhanced threat prediction with deception data"""
            prediction = original_predict_threat(data)
            
            # If deception is active and has detected activity, increase threat score
            if hasattr(omega_server, 'deception_engine'):
                if omega_server.deception_engine.is_active:
                    stats = omega_server.deception_engine.get_deception_stats()
                    if stats['unique_attackers'] > 0:
                        # Increase threat score based on deception activity
                        deception_factor = min(0.3, stats['unique_attackers'] * 0.05)
                        prediction['threat_score'] = min(1.0, prediction['threat_score'] + deception_factor)
                        prediction['factors'].append(f"Deception traps triggered: {stats['unique_attackers']}")
            
            return prediction
        
        omega_server.threat_predictor.predict = enhanced_predict_threat
    
    print("✅ Deception Engine integrated successfully")
    return omega_server

