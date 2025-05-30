pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Cloning Repo') {
            steps {
                script {
                    echo 'Cloning GitHub repository...'
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

        stage('Check Python Setup') {
            steps {
                script {
                    bat """
                    where python
                    python --version
                    """
                }
            }
        }

        stage('Set Up Virtual Environment') {
            steps {
                script {
                    bat """
                    python -m venv %VENV_DIR%
                    call %VENV_DIR%\\Scripts\\activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    """
                }
            }
        }

        stage('Success Message') {
            steps {
                script {
                    bat "echo 🎉 Jenkins pipeline with virtual environment completed!"
                }
            }
        }
    }
}
