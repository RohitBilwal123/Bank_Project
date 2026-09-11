pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
            }
        }

        stage('Test') {
            steps {
                echo 'Running Python tests...'
                bat 'python -m pytest'
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'
                bat 'docker build -t bank-project .'
            }
        }

        stage('Docker Deploy') {
            steps {
                echo 'Deploying application...'
                bat 'docker rm -f bank-app 2>nul'
                bat 'docker run -d -p 5000:5000 --name bank-app bank-project'
            }
        }

        stage('Verify') {
            steps {
                echo 'Checking Docker container...'
                bat 'docker ps'
            }
        }
    }

    post {
        success {
            echo 'CI/CD Pipeline completed successfully!'
        }

        failure {
            echo 'CI/CD Pipeline failed!'
        }
    }
}