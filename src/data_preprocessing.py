# Import standard libraries
import os  # For interacting with the operating system and file paths
import pandas as pd  # For data loading and manipulation
import numpy as np  # For numerical operations (e.g., log transformation)
import sys

# Import custom utilities and configuration
from src.logger import get_logger  # Custom logger to log info, warnings, and errors
from src.custom_exception import CustomException  # Custom exception class for clean error handling
from config.paths_config import *  # Load file paths used in the pipeline (train/test/config)
from utils.common_functions import read_yaml, load_data  # Helper functions for reading config and loading data

# Import machine learning and preprocessing libraries
from sklearn.ensemble import RandomForestClassifier  # For feature importance-based selection
from sklearn.preprocessing import LabelEncoder  # For encoding categorical variables
from imblearn.over_sampling import SMOTE  # For balancing imbalanced datasets

# Initialize the logger for this module
logger = get_logger(__name__)

# Define a class for data processing operations
class DataProcessor:

    # Initialize class with data paths and config file
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path  # Path to training data
        self.test_path = test_path  # Path to testing data
        self.processed_dir = processed_dir  # Output directory for processed data

        # Load YAML config for preprocessing parameters
        self.config = read_yaml(config_path)

        # Create processed directory if it does not exist
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    # Method for preprocessing: drop columns, encode, fix skewness
    def preprocess_data(self, df):
        try:
            logger.info("Starting our Data Processing step")

            # Drop irrelevant or unneeded columns
            logger.info("Dropping the columns")
            df.drop(columns=['Unnamed: 0', 'Booking_ID'], inplace=True, errors='ignore')

            df.drop_duplicates(inplace=True)  # Remove duplicate rows

            # Get categorical and numerical column names from config
            cat_cols = self.config["data_processing"]["categorical_columns"]
            num_cols = self.config["data_processing"]["numerical_columns"]

            # Log the start of label encoding
            logger.info("Applying Label Encoding")
            label_encoder = LabelEncoder()  # Initialize label encoder
            mappings = {}  # To store category-to-code mappings

            # Apply label encoding to each categorical column
            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])  # Replace categories with numbers
                mappings[col] = {
                    label: code for label, code in zip(
                        label_encoder.classes_,
                        label_encoder.transform(label_encoder.classes_)
                    )
                }

            # Log encoded label mappings for traceability
            logger.info("Label Mappings are:")
            for col, mapping in mappings.items():
                logger.info(f"{col} : {mapping}")

            # Handle skewed numerical features by applying log1p
            logger.info("Doing Skewness Handling")
            skew_threshold = self.config["data_processing"]["skewness_threshold"]  # Skew threshold from config
            skewness = df[num_cols].apply(lambda x: x.skew())  # Calculate skewness for numeric columns

            # Log transform skewed columns
            for column in skewness[skewness > skew_threshold].index:
                df[column] = np.log1p(df[column])  # log1p handles zero values safely

            return df  # Return the cleaned DataFrame

        except Exception as e:
            logger.error(f"Error during preprocess step: {e}")
            raise CustomException("Error while preprocessing data", sys)


    # Method to balance classes using SMOTE
    def balance_data(self, df):
        try:
            logger.info("Handling Imbalanced Data")

            # Separate features and target variable
            X = df.drop(columns='booking_status')
            y = df["booking_status"]

            # Apply SMOTE to oversample minority class
            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X, y)

            # Combine resampled features and target into a new DataFrame
            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df["booking_status"] = y_resampled

            logger.info("Data balanced successfully")
            return balanced_df

        except Exception as e:
            logger.error(f"Error during balancing data step: {e}")
            raise CustomException("Error while balancing data", sys)

    # Method to select top N important features using Random Forest
    def select_features(self, df):
        try:
            logger.info("Starting our Feature selection step")

            # Split into features and target
            X = df.drop(columns='booking_status')
            y = df["booking_status"]

            # Train Random Forest to determine feature importance
            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)

            feature_importance = model.feature_importances_  # Get importance scores

            # Create a DataFrame of features and their importance
            feature_importance_df = pd.DataFrame({
                'feature': X.columns,
                'importance': feature_importance
            })

            # Sort features by importance (highest first)
            top_features_importance_df = feature_importance_df.sort_values(by="importance", ascending=False)

            # Get number of top features to select from config
            num_features_to_select = self.config["data_processing"]["no_of_features"]
            top_10_features = top_features_importance_df["feature"].head(num_features_to_select).values

            logger.info(f"Features selected: {top_10_features}")

            # Keep only top features and target in the final DataFrame
            top_10_df = df[top_10_features.tolist() + ["booking_status"]]

            logger.info("Feature selection completed successfully")
            return top_10_df

        except Exception as e:
            logger.error(f"Error during feature selection step: {e}")
            raise CustomException("Error while feature selection", e)

    # Save processed data to CSV file
    def save_data(self, df, file_path):
        try:
            logger.info("Saving our data in processed folder")
            df.to_csv(file_path, index=False)  # Save DataFrame to CSV without index
            logger.info(f"Data saved successfully to {file_path}")
        except Exception as e:
            logger.error(f"Error during saving data step: {e}")
            raise CustomException("Error while saving data", sys)

    # Main processing pipeline: load → preprocess → balance → select → save
    def process(self):
        try:
            logger.info("Loading data from RAW directory")

            # Load training and test data
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            # Preprocess both datasets
            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            # Balance both datasets (if needed)
            train_df = self.balance_data(train_df)
            test_df = self.balance_data(test_df)

            # Select important features from training set
            train_df = self.select_features(train_df)

            # Align test set columns to match selected features
            test_df = test_df[train_df.columns]

            # Save processed train and test datasets to disk
            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)

            logger.info("Data processing completed successfully")

        except Exception as e:
            logger.error(f"Error during preprocessing pipeline: {e}")
            raise CustomException("Error while running data preprocessing pipeline", sys)

# Run the data processing pipeline when this file is executed
if __name__ == "__main__":
    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process()
