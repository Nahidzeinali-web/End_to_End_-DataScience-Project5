
# 🧪 Data Ingestion Pipeline with Google Cloud Storage and Train/Test Splitting

This project demonstrates an automated data ingestion pipeline that:
- Downloads a CSV dataset from a Google Cloud Storage (GCS) bucket,
- Saves the file locally,
- Splits the data into train and test sets,
- Logs the entire process using a custom logger,
- Handles exceptions using a custom exception class.

---

## 📁 Project Structure

```
project-root/
│
├── src/
│   ├── logger.py               # Custom logger setup
│   ├── custom_exception.py     # Custom exception class
│
├── config/
│   ├── paths_config.py         # Constants for paths (RAW_DIR, TRAIN_FILE_PATH, etc.)
│   └── config.yaml             # Configuration file (bucket name, filename, split ratio)
│
├── utils/
│   └── common_functions.py     # Utility functions (e.g., read_yaml)
│
├── data/                       # Stores downloaded and split datasets
│   ├── raw/
│   ├── train/
│   └── test/
│
├── main.py                     # Entry point to run the pipeline
└── README.md                   # You are here
```

---

## ⚙️ Configuration (`config.yaml`)

```yaml
data_ingestion:
  bucket_name: "your-gcp-bucket-name"
  bucket_file_name: "your-data.csv"
  train_ratio: 0.8
```

---

## 🛠 How It Works

1. **Read config** from `config.yaml` using `read_yaml`.
2. **Download CSV** from GCP using the `google-cloud-storage` client.
3. **Save it locally** in the `raw/` directory.
4. **Split the dataset** into training and testing sets using `scikit-learn`.
5. **Store results** in `train/` and `test/` directories.
6. **Log messages** during each step, including timestamps, using a custom logger.
7. **Handle errors** gracefully using a `CustomException`.


