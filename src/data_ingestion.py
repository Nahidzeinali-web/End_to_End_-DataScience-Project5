# Import required libraries
import os  # For file and directory operations
import pandas as pd  # For reading and manipulating CSV files
from google.cloud import storage  # To interact with Google Cloud Storage
from sklearn.model_selection import train_test_split  # For splitting dataset into train and test sets
from src.logger import get_logger  # Custom logger for structured logging
from src.custom_exception import CustomException  # Custom exception handling
from config.paths_config import *  # File path constants (e.g., RAW_FILE_PATH, TRAIN_FILE_PATH, etc.)
from utils.common_functions import read_yaml  # Utility function to read YAML configuration files
import sys  # For extracting exception traceback

# Initialize logger instance
logger = get_logger(__name__)

# Define the DataIngestion class to manage data retrieval and preparation
class DataIngestion:
    def __init__(self, config):
        """
        Initialize the DataIngestion class with config values.
        Extracts the bucket name, file name, and train-test split ratio.
        Ensures raw data directory exists.
        """
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]

        # Create the raw data directory if it does not exist
        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info(f"Data Ingestion started with {self.bucket_name} and file is {self.file_name}")

    def download_csv_from_gcp(self):
        """
        Downloads a CSV file from a Google Cloud Storage bucket and saves it locally.
        Requires Application Default Credentials or a service account key to be set.
        """
        try:
            # Create a Google Cloud Storage client (requires proper credentials)
            client = storage.Client()

            # Access the specified bucket
            bucket = client.bucket(self.bucket_name)

            # Reference the file (blob) inside the bucket
            blob = bucket.blob(self.file_name)

            # Download the file to the specified RAW_FILE_PATH
            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f"CSV file successfully downloaded to {RAW_FILE_PATH}")

        except Exception as e:
            logger.error("Error while downloading the CSV file from GCP")
            raise CustomException("Failed to download CSV file", sys)

    def split_data(self):
        """
        Splits the raw dataset into training and testing datasets and saves them.
        """
        try:
            logger.info("Starting the data splitting process")

            # Read the downloaded CSV file into a pandas DataFrame
            data = pd.read_csv(RAW_FILE_PATH)

            # Split the data using the configured ratio
            train_data, test_data = train_test_split(data, test_size=1 - self.train_test_ratio, random_state=42)

            # Save the train and test data to specified file paths
            train_data.to_csv(TRAIN_FILE_PATH, index=False)
            test_data.to_csv(TEST_FILE_PATH, index=False)

            logger.info(f"Train data saved to {TRAIN_FILE_PATH}")
            logger.info(f"Test data saved to {TEST_FILE_PATH}")

        except Exception as e:
            logger.error("Error while splitting data")
            raise CustomException("Failed to split data into training and test sets", sys)

    def run(self):
        """
        Orchestrates the full data ingestion process: download and split.
        """
        try:
            logger.info("Starting data ingestion process")

            # Step 1: Download the CSV file from GCP
            self.download_csv_from_gcp()

            # Step 2: Split the downloaded data
            self.split_data()

            logger.info("Data ingestion completed successfully")

        except CustomException as ce:
            logger.error(f"CustomException occurred during data ingestion: {str(ce)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise CustomException("Unexpected error during data ingestion", sys)
        finally:
            logger.info("Data ingestion process finalized")  # This always runs

# If this script is run directly, perform data ingestion using config from YAML
if __name__ == "__main__":
    try:
        # Read configuration from the YAML file
        config = read_yaml(CONFIG_PATH)

        # Run the ingestion process
        data_ingestion = DataIngestion(config)
        data_ingestion.run()

    except Exception as e:
        logger.error("Failed to initialize or run data ingestion")
        raise CustomException("Fatal error in data ingestion __main__ block", sys)
