pipeline {
    agent any

    stages {
        stage('Cloning GitHub repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning GitHub repo to Jenkins............'
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

        stage('Installing dependencies without venv') {
            steps {
                script {
                    echo 'Installing dependencies directly using pip............'
                    sh '''
                    python3 --version
                    pip3 install --upgrade pip
                    pip3 install -r requirements.txt
                    '''
                }
            }
        }
    }
}
