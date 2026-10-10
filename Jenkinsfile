
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Test') {
            steps {
                echo 'Checking Python installation...'
                bat 'where python'
                bat 'python --version'

                echo 'Installing test dependencies...'
                bat 'python -m pip install pytest'

                echo 'Running Python tests...'
                bat 'python -m pytest --junitxml=test-results.xml'
            }
            post {
                always {
                    junit allowEmptyResults: true,
                          testResults: 'test-results.xml'
                }
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
                echo 'Removing old container if present...'
                bat 'docker rm -f bank-app 2>nul || exit /b 0'

                echo 'Starting application container...'
                bat 'docker run -d -p 5000:5000 --name bank-app bank-project'
            }
        }

        stage('Verify') {
            steps {
                echo 'Checking Docker container...'
                bat 'docker ps --filter "name=bank-app"'
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
