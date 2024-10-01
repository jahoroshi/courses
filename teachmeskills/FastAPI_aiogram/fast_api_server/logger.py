import logging
import sys
from logging.handlers import TimedRotatingFileHandler

# Create a logger instance
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

# Log format
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Handler for console output
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Handler for writing logs to a file with daily rotation
file_handler = TimedRotatingFileHandler(
    "logs/app.log", when="midnight", interval=1
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
file_handler.suffix = "%Y%m%d"  # Add date to the log file name

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
