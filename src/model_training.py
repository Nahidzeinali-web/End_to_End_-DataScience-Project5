# Standard library imports
import os  # For file and directory handling

# Data and model-related imports
import pandas as pd  # For data manipulation
import joblib  # For saving/loading trained model objects

# Model selection and evaluation
from sklearn.model_selection import RandomizedSearchCV  # For hyperparameter tuning
import lightgbm as lgb  # LightGBM model for classification
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score  # For model evaluation

# Project-specific modules
from src.logger import get_logger  # Custom logger utility
from src.custom_exception import CustomException  # Custom exception handling
from config.paths_config import *  # File paths for training/test data and output
from config.model_params import *  # LightGBM and RandomSearch parameter configs
from utils.common_functions import read_yaml, load_data  # Utility functions to read YAML config and load data
from scipy.stats import randint  # For defining hyperparameter ranges (used in model_params)

# MLflow for tracking experiments
import mlflow
import mlflow.sklearn

# Initialize the logger for this module
logger = get_logger(__name__)

# Define a class for the model training pipeline
class ModelTraining:

    # Initialize with training/test file paths and output model save path
    def __init__(self, train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        # Load parameter grids from config
        self.params_dist = LIGHTGM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    # Load data and split it into features (X) and labels (y)
    def load_and_split_data(self):
        try:
            logger.info(f"Loading data from {self.train_path}")
            train_df = load_data(self.train_path)

            logger.info(f"Loading data from {self.test_path}")
            test_df = load_data(self.test_path)

            # Split train and test into X (features) and y (labels)
            X_train = train_df.drop(columns=["booking_status"])
            y_train = train_df["booking_status"]
            X_test = test_df.drop(columns=["booking_status"])
            y_test = test_df["booking_status"]

            logger.info("Data split successfully for Model Training")

            return X_train, y_train, X_test, y_test
        except Exception as e:
            logger.error(f"Error while loading data {e}")
            raise CustomException("Failed to load data", e)

    # Train LightGBM model with hyperparameter tuning
    def train_lgbm(self, X_train, y_train):
        try:
            logger.info("Initializing our model")

            # Define base LightGBM model
            lgbm_model = lgb.LGBMClassifier(random_state=self.random_search_params["random_state"])

            logger.info("Starting our Hyperparameter tuning")

            # Define randomized search with specified parameters
            random_search = RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.params_dist,
                n_iter=self.random_search_params["n_iter"],
                cv=self.random_search_params["cv"],
                n_jobs=self.random_search_params["n_jobs"],
                verbose=self.random_search_params["verbose"],
                random_state=self.random_search_params["random_state"],
                scoring=self.random_search_params["scoring"]
            )

            # Fit randomized search to training data
            random_search.fit(X_train, y_train)

            logger.info("Hyperparameter tuning completed")

            # Extract best model and params
            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_

            logger.info(f"Best parameters are: {best_params}")

            return best_lgbm_model

        except Exception as e:
            logger.error(f"Error while training model {e}")
            raise CustomException("Failed to train model", e)

    # Evaluate trained model on test data
    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info("Evaluating our model")

            # Make predictions
            y_pred = model.predict(X_test)

            # Calculate evaluation metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            # Log each metric
            logger.info(f"Accuracy Score: {accuracy}")
            logger.info(f"Precision Score: {precision}")
            logger.info(f"Recall Score: {recall}")
            logger.info(f"F1 Score: {f1}")

            # Return metrics as a dictionary
            return {
                "accuracy": accuracy,
                "precison": precision,
                "recall": recall,
                "f1": f1
            }

        except Exception as e:
            logger.error(f"Error while evaluating model {e}")
            raise CustomException("Failed to evaluate model", e)

    # Save the trained model to disk using joblib
    def save_model(self, model):
        try:
            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)

            logger.info("Saving the model")
            joblib.dump(model, self.model_output_path)  # Save model
            logger.info(f"Model saved to {self.model_output_path}")
        except Exception as e:
            logger.error(f"Error while saving model {e}")
            raise CustomException("Failed to save model", e)

    # Main function that executes the full pipeline
    def run(self):
        try:
            # Start MLflow experiment run
            with mlflow.start_run():
                logger.info("Starting our Model Training pipeline")

                # Log data files used in this experiment
                logger.info("Logging the training and testing dataset to MLflow")
                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                # Load, train, evaluate, and save
                X_train, y_train, X_test, y_test = self.load_and_split_data()
                best_lgbm_model = self.train_lgbm(X_train, y_train)
                metrics = self.evaluate_model(best_lgbm_model, X_test, y_test)
                self.save_model(best_lgbm_model)

                # Log model and metrics to MLflow
                logger.info("Logging the model into MLflow")
                mlflow.log_artifact(self.model_output_path)

                logger.info("Logging Params and metrics to MLflow")
                mlflow.log_params(best_lgbm_model.get_params())
                mlflow.log_metrics(metrics)

                logger.info("Model Training successfully completed")

        except Exception as e:
            logger.error(f"Error in model training pipeline {e}")
            raise CustomException("Failed during model training pipeline", e)

# Run the training pipeline if this file is executed directly
if __name__ == "__main__":
    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
    trainer.run()
