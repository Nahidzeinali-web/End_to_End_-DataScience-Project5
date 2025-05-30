
# 🏨 Hotel Reservation Prediction Pipeline

This project demonstrates a comprehensive machine learning pipeline for reservation prediction, utilizing Python. It incorporates modular code design, experiment tracking, CI/CD, and containerization, making it suitable for production-ready deployment.

## 📁 Project Structure

```
PROJECT CODE/
│
├── application.py              # Main app interface (Flask/FastAPI)
├── requirements.txt            # Python dependencies
├── Dockerfile                  # For containerizing the app
├── Jenkinsfile                 # CI/CD automation with Jenkins
├── setup.py                    # Package setup file
│
├── config/                     # Configuration files and constants
│   ├── config.yaml             # Central YAML configuration
│   ├── model_params.py         # Model hyperparameters
│   ├── paths_config.py         # File path constants
│   └── __init__.py
│
├── data/                       # Processed datasets
├── src/                        # Core codebase (models, utils, etc.)
│   ├── data_loader.py
│   ├── model_trainer.py
│   ├── logger.py
│   └── custom_exception.py
│
└── artifacts/                  # Saved models and results
```

## 🔧 Features

- **Data Preprocessing:** Loads and cleans hotel review data.
- **Model Training:** Trains machine learning models (e.g., Random Forest, Logistic Regression).
- **Evaluation:** Includes metrics such as accuracy, precision, recall, and confusion matrix.
- **CI/CD:** Jenkins integration for continuous deployment.
- **Dockerized:** Easily deployable using Docker.
- **Logging & Exceptions:** Robust error handling and custom logging.
- **Modular Design:** Clear separation of configuration, code, and data.

## 🚀 Getting Started

### Prerequisites

Install required packages:

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python application.py
```


