import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_file = os.path.join(log_dir, "job_watcher.log")
    
    # Configure logger
    logger = logging.getLogger("JobWatcher")
    logger.setLevel(logging.INFO)
    
    # Check if handlers already exist to avoid duplicate handlers
    if not logger.handlers:
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler (rotates at 5MB, keeps 3 backups)
        file_handler = RotatingFileHandler(
            log_file, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        
        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

# Create global logger instance
logger = setup_logger()
