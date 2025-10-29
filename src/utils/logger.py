import logging
import os
from datetime import datetime
from pathlib import Path

def setup_logger(name, log_file=None, level=logging.INFO):
    """Setup logger with file and console handlers"""
    
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding multiple handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = logs_dir / f"{name}_{timestamp}.log"
    else:
        log_file = logs_dir / log_file
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

def get_main_logger():
    """Get the main application logger"""
    return setup_logger("agentic_framework", "main.log")

def get_agent_logger(agent_name):
    """Get logger for specific agent"""
    return setup_logger(f"agent_{agent_name}", f"agent_{agent_name}.log")

def get_api_logger():
    """Get logger for API calls"""
    return setup_logger("api_calls", "api_calls.log")

def log_function_call(logger, func_name, *args, **kwargs):
    """Log function calls with parameters"""
    logger.info(f"Calling function: {func_name}")
    if args:
        logger.debug(f"Args: {args}")
    if kwargs:
        logger.debug(f"Kwargs: {kwargs}")

def log_api_response(logger, api_name, status_code, response_text=None):
    """Log API responses"""
    logger.info(f"{api_name} API - Status: {status_code}")
    if response_text:
        logger.debug(f"{api_name} Response: {response_text[:500]}...")  # Truncate long responses
