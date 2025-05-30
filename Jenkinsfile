pipeline {
    agent any

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Nahidzeinali-web/End_to_End_-DataScience-Project5.git']])
                }
            }
        }

  }
}
