pipeline{
    agent any

    environment{
        VENV_DIR='venv'
    }
    stages{

        stage('Cloning Github repo to Jenkins'){
            steps{
                echo 'Cloning Github repo to Jenkins...'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Nahidzeinali-web/End_to_End_-DataScience-Project5.git']])
            }
        }

         stage('Setting up our Virtual Environment and Installing Dependancies'){
            steps{
                echo 'Setting up our Virtual Environment and Installing Dependancies...'
                sh '''
                python -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate
                pip install --upgrage pip
                pip install -e .
                '''
            }
        }
    }
}