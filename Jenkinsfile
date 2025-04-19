pipeline {
    agent any

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                // Install dependencies if you have any, like using pip
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Script') {
            steps {
                // Adjusting the path to main.py if it's inside the 'app' folder
                bat 'python app\\main.py'
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution finished.'
        }

        failure {
            echo 'Build failed!'
        }
    }
}
