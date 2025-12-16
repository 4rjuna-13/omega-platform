"""
DECEPTION -> RESPONSE INTEGRATION
Links the Deception Engine to Autonomous Response
"""

def integrate_deception_with_response(deception_engine, response_engine):
    """Link deception events to response system"""
    
    # Store original method
    original_log_event = deception_engine.log_deception_event
    
    def enhanced_log_event(honeypot_id, event_type, source_ip, details, severity):
        # Call original method
        original_log_event(honeypot_id, event_type, source_ip, details, severity)
        
        # Trigger response system if active
        if response_engine.is_active:
            threat_data = {
                'event_type': event_type,
                'source_ip': source_ip,
                'details': details,
                'severity': severity,
                'honeypot_id': honeypot_id,
                'timestamp': deception_engine.deception_log[-1]['timestamp'] if deception_engine.deception_log else 'unknown'
            }
            
            # Handle the threat
            response_result = response_engine.handle_threat(threat_data)
            
            # Log the integration
            deception_engine.logger.info(f"Deception→Response: {event_type} from {source_ip} triggered response")
    
    # Replace the method
    deception_engine.log_deception_event = enhanced_log_event
    
    print("[INTEGRATION] Deception Engine linked to Autonomous Response")

