import logging
import sys
import os
from logging.handlers import RotatingFileHandler
import config

# Rule 10: Observability (Logs + Metrics)
# We use a RotatingFileHandler to ensure logs don't eat the entire hard drive.

def setup_logger(name: str = "mr_assistant"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 1. Console Handler (For Dev)
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    # 2. File Handler (For Production/Durable history)
    import pathlib
    log_dir = pathlib.Path(config.config.LOGS_DIR)
    os.makedirs(log_dir, exist_ok=True)
    log_file = log_dir / "app.log"
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8" # 5MB per file, keep 3
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger

# Singleton instance
logger = setup_logger()
