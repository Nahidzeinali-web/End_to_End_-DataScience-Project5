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
---

## ⚙️ Jenkins and Docker Setup (Local)

### 1. Install Docker

- Download Docker Desktop from the official website and **run it in the background**.

### 2. Set up Jenkins in Docker

#### Create Jenkins Setup

- Make a folder `custom_jenkins`
- Inside it, create a `Dockerfile` with the following content:

```dockerfile
FROM jenkins/jenkins:lts

USER root

RUN apt-get update -y && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    echo "deb [arch=amd64] https://download.docker.com/linux/debian bullseye stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean

RUN groupadd -f docker && \
    usermod -aG docker jenkins

RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

USER jenkins
```

#### Build and Run Jenkins Container

```bash
cd custom_jenkins
docker build -t jenkins-dind .
docker images

docker run -d-- name jenkins-dind ^
--privileged ^
-p 8080:8080 -p 50000:50000 ^
-v //var/run/docker.sock:/var/run/docker.sock ^
-v jenkins_home:/var/jenkins_home ^
jenkins-dind
```

Check if it's running:

```bash
docker ps
docker logs jenkins-dind
```

Copy the Jenkins initial admin password from the logs and open your browser:

- Go to: `http://localhost:8080`
- Paste the password
- Install suggested plugins
- Create your admin user

### 3. Enable Python in Jenkins Container

```bash
docker exec -u root -it jenkins-dind bash
apt update -y
apt install -y python3
ln -s /usr/bin/python3 /usr/bin/python
apt install -y python3-pip python3-venv
exit

docker restart jenkins-dind
```

### 4. Project Container Setup

Create a separate `Dockerfile` for your Python project:

```dockerfile
FROM python:slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -e .

RUN python pipeline/training_pipeline.py

EXPOSE 5000

CMD ["python", "application.py"]
```

### 5. Install Google Cloud CLI in Jenkins Container

```bash
docker exec -u root -it jenkins-dind bash

apt-get update
apt-get install -y curl apt-transport-https ca-certificates gnupg

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

apt-get update && apt-get install -y google-cloud-sdk
gcloud --version
exit
```

### 6. Grant Docker Permissions to Jenkins

```bash
docker exec -u root -it jenkins-dind bash
groupadd docker
usermod -aG docker jenkins
usermod -aG root jenkins
exit

docker restart jenkins-dind
```

> ✅ Now Jenkins is ready to automate builds, and your app is Dockerized for deployment.

🎥 Check tutorial videos for the remaining steps. You can always copy code from this guide as needed.
=======

>>>>>>> b97a025bc36a7a4c7f96be4b6ee85f74851e0a04
