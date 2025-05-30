pipeline {
    agent any

    stages {
        stage('Clone GitHub Repo') {
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

        stage('Install Dependencies (no venv, override PEP 668)') {
            steps {
                script {
                    echo '📦 Installing dependencies using pip with --break-system-packages...'
                    sh '''
                    python3 --version
                    pip3 install --upgrade pip --break-system-packages
                    pip3 install --break-system-packages -r requirements.txt
                    '''
                }
            }
        }

        stage('✅ Pipeline Complete') {
            steps {
                script {
                    sh 'echo "🎉 All done! Dependencies installed."'
                }
            }
        }
    }
}
