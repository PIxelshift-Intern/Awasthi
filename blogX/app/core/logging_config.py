import os
import logging
from logging.handlers import RotatingFileHandler

logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
os.makedirs(logs_dir, exist_ok=True)

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    
    log_file = os.path.join(logs_dir, 'blogX.log')
    f_handler = RotatingFileHandler(
        log_file, 
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    f_handler.setLevel(logging.INFO)
    
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(log_format)
    f_handler.setFormatter(log_format)
    
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    
    return logger 