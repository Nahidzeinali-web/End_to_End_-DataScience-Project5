pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Clone Repo') {
            steps {
                script {
                    echo '🔄 Cloning GitHub repository...'
                    checkout scmGit(
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'github-token',
                            url: 'https://github.com/Nahidzeinali-web/End_to_End_-DataScience-Project5.git'
                        ]]
                    )
                }
            }
        }

        stage('Diagnose Python') {
            steps {
                script {
                    bat """
                    echo 🔍 Checking Python location and version...
                    where python
                    python --version
                    """
                }
            }
        }

        stage('List Files') {
            steps {
                script {
                    bat """
                    echo 📁 Listing workspace files...
                    dir
                    type requirements.txt
                    """
                }
            }
        }

        stage('Create Venv + Install Dependencies') {
            steps {
                script {
                    bat """
                    echo 🛠 Creating virtual environment...
                    python -m venv %VENV_DIR%

                    echo 🔄 Activating environment + installing requirements...
                    call %VENV_DIR%\\Scripts\\activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    """
                }
            }
        }

        stage('Done') {
            steps {
                script {
                    bat "echo ✅ Jenkins pipeline completed successfully!"
                }
            }
        }
    }
}
