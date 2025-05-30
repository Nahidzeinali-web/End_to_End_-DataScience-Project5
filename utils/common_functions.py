# Import necessary libraries
import os  # For interacting with the file system
import pandas as pd  # For data manipulation (used in load_data function)
from src.logger import get_logger  # Custom function to get a logger instance
from src.custom_exception import CustomException  # Custom exception class for better error tracking
import yaml  # For reading YAML configuration files

# Initialize a logger for the current module
logger = get_logger(__name__)

# Function to read a YAML configuration file and return its contents as a dictionary
def read_yaml(fil_path):
    try:
        # Check if the given file path exists
        if not os.path.exists(fil_path):
            # If not, raise a FileNotFoundError
            raise FileNotFoundError("File is not at the given path")
        
        # Open the YAML file in read mode
        with open(fil_path, "r") as yaml_file:
            # Parse the YAML file safely and load its contents into a dictionary
            config = yaml.safe_load(yaml_file)
            # Log a message indicating successful reading
            logger.info("Successfully read the YAML file")
            return config  # Return the parsed configuration data

    except Exception as e:
        # Log an error message if something goes wrong
        logger.error("Error while reading the YAML file")
        # Raise a custom exception with context
        raise CustomException("Failed to read YAML file")

# Function to load data from a CSV file
def load_data(path):
    try:
        # Log that data loading has started
        logger.info("Loading data")
        # Read the CSV file into a pandas DataFrame and return it
        return pd.read_csv(path)
    
    except Exception as e:
        # Log an error message with the exception details
        logger.error(f"Error loading the data: {e}")
        # Raise a custom exception for higher-level error handling
        raise CustomException("Failed to load data", e)
