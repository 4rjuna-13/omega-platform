#!/usr/bin/env python3
"""
Omega Platform - Main Entry Point
Usage: python -m omega_platform [command] [options]
"""

import sys
import argparse
from omega_platform.core.engine import OmegaEngine
from omega_platform.core.config_loader import load_config
from omega_platform.core.logging_setup import setup_logging

def start_dashboard(args):
    """Start the simulation dashboard"""
    try:
        from omega_platform.web.dashboard.simulation_app import app
        
        host = args.host if hasattr(args, 'host') else '0.0.0.0'
        port = args.port if hasattr(args, 'port') else 5000
        debug = args.debug if hasattr(args, 'debug') else False
        
        print(f"🚀 Starting Omega Platform Simulation Dashboard...")
        print(f"   URL: http://{host}:{port}")
        print(f"   Debug mode: {debug}")
        print("   Press Ctrl+C to stop")
        
        app.run(host=host, port=port, debug=debug)
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("Please install required packages:")
        print("  pip install flask")
        return 1

def main():
    """Main entry point for Omega Platform"""
    parser = argparse.ArgumentParser(description="Omega Security Platform")
    parser.add_argument("--config", "-c", default="config/defaults.yaml",
                       help="Configuration file path")
    parser.add_argument("--env", "-e", default="development",
                       help="Environment: development, staging, production")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Start command
    start_parser = subparsers.add_parser('start', help='Start the Omega Platform')
    
    # Stop command
    stop_parser = subparsers.add_parser('stop', help='Stop the Omega Platform')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Check platform status')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Run tests')
    
    # Version command
    version_parser = subparsers.add_parser('version', help='Show version')
    
    # Dashboard command
    dashboard_parser = subparsers.add_parser('dashboard', help='Start simulation dashboard')
    dashboard_parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    dashboard_parser.add_argument('--port', type=int, default=5000, help='Port to listen on')
    dashboard_parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Setup logging first
    setup_logging()
    
    # If no command specified, default to start
    if args.command is None:
        args.command = 'start'
    
    # Execute command
    if args.command == "dashboard":
        return start_dashboard(args)
    
    # For other commands, load the engine
    config = load_config(args.config, args.env)
    engine = OmegaEngine(config)
    
    if args.command == "start":
        engine.start()
    elif args.command == "stop":
        engine.stop()
    elif args.command == "status":
        engine.status()
    elif args.command == "test":
        engine.run_tests()
    elif args.command == "version":
        print(f"Omega Platform v{engine.get_version()}")
    else:
        print(f"Unknown command: {args.command}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
