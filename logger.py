"""
Logging configuration for Resume Relevance Check System
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

def setup_logging():
    """Setup structured logging"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler
    file_handler = logging.FileHandler(
        log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger

def log_info(message: str):
    """Log info message"""
    logging.info(message)

def log_error(message: str):
    """Log error message"""
    logging.error(message)

def log_warning(message: str):
    """Log warning message"""
    logging.warning(message)

def log_debug(message: str):
    """Log debug message"""
    logging.debug(message)

# Initialize logger
logger = setup_logging()
