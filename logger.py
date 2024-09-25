import logging
import os

def setup_logger(name: str, log_file: str, level=logging.INFO):
    """
    Sets up a logger with the specified name, log file, and logging level.
    
    Args:
        name (str): Name of the logger.
        log_file (str): File path for the log file.
        level (int): Logging level (e.g., logging.INFO, logging.ERROR).
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')

    # Ensure the log directory exists
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(stream_handler)

    return logger

# Initialize the main logger
main_logger = setup_logger('main_logger', 'logs/application.log')