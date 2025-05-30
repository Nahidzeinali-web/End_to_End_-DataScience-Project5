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

        stage('Check Python') {
            steps {
                script {
                    sh '''
                    echo "🔍 Checking Python..."
                    which python3
                    python3 --version
                    '''
                }
            }
        }

        stage('List Files') {
            steps {
                script {
                    sh '''
                    echo "📁 Listing workspace files..."
                    ls -l
                    cat requirements.txt
                    '''
                }
            }
        }

        stage('Create Virtual Environment and Install Dependencies') {
            steps {
                script {
                    sh '''
                    echo "🛠 Creating virtual environment..."
                    python3 -m venv ${VENV_DIR}
                    source ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Done') {
            steps {
                script {
                    sh 'echo ✅ Jenkins pipeline completed successfully!'
                }
            }
        }
    }
}
