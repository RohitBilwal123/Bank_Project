pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Python Version') {
            steps {
                bat '"C:\\Users\\rohit\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" --version'
            }
        }

        stage('Compile') {
            steps {
                bat '"C:\\Users\\rohit\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" -m py_compile main.py banking\\account.py banking\\transactions.py'
            }
        }

        stage('Build Success') {
            steps {
                echo 'Python Bank Project compilation successful!'
            }
        }
    }
}