import os
"""
Structured JSON logging setup for Omega Platform
"""

import logging
import json
import sys
from datetime import datetime
from pythonjsonlogger import jsonlogger

class StructuredJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter for structured logging"""
    
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        
        # Add standard fields
        log_record['timestamp'] = datetime.utcnow().isoformat() + 'Z'
        log_record['level'] = record.levelname
        log_record['logger'] = record.name
        
        # Add process/thread info
        log_record['pid'] = record.process
        log_record['thread'] = record.threadName
        
        # Remove default fields we don't want
        log_record.pop('message', None)
        log_record.pop('asctime', None)
        
        # Rename msg to message
        if 'msg' in log_record:
            log_record['message'] = log_record.pop('msg')

def setup_logging(log_level: str = "INFO", json_format: bool = True):
    """
    Setup logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: Whether to use JSON formatting (for production) or plain text
    """
    
    # Convert string log level to logging constant
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    
    if json_format:
        # JSON format for structured logging
        formatter = StructuredJsonFormatter(
            '%(timestamp)s %(level)s %(logger)s %(message)s'
        )
    else:
        # Plain text format for development
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Create file handler for JSON logs (always JSON)
    try:
        os.makedirs("logs", exist_ok=True)
        file_handler = logging.FileHandler("logs/omega_platform.log")
        file_formatter = StructuredJsonFormatter(
            '%(timestamp)s %(level)s %(logger)s %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not setup file logging: {e}")
    
    # Set specific loggers to higher/lower levels
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    
    logging.info(f"Logging configured with level: {log_level}, JSON format: {json_format}")
