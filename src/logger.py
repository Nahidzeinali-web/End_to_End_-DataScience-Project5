# Import the logging module to log messages for debugging or monitoring
import logging

# Import os to work with directories and paths
import os

# Import datetime to generate timestamped log filenames
from datetime import datetime


# Define the directory where all log files will be saved
LOGS_DIR = "logs"

# Create the 'logs' directory if it doesn't already exist
os.makedirs(LOGS_DIR, exist_ok=True)  # `exist_ok=True` prevents error if directory already exists

# Generate a log file name with the current date, e.g., log_2025-05-29.log
LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

# Configure the logging system
logging.basicConfig(
    filename=LOG_FILE,  # Save logs to the specified file
    format='%(asctime)s-%(levelname)s-%(message)s',  # Format includes timestamp, log level, and message
    level=logging.INFO  # Set the minimum severity level to INFO (DEBUG < INFO < WARNING < ERROR < CRITICAL)
)


# Define a helper function to create/get a named logger instance
def get_logger(name):
    # Create or retrieve a logger with the specified name
    logger = logging.getLogger(name)

    # Set the logger’s level to INFO so it captures info-level logs and above
    logger.setLevel(logging.INFO)

    # Return the configured logger
    return logger
