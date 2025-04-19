pipeline {
    agent any

    environment {
        PYTHON_PATH = "C:\\Program Files\\Python312\\python.exe"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Renukakadam/Image-Compressor.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'call "%PYTHON_PATH%" -m venv venv && venv\\Scripts\\activate && pip install -r requirements.txt'
            }
        }

        stage('Run Script') {
            steps {
                bat 'call venv\\Scripts\\activate && python main.py'
            }
        }
    }

    post {
        success {
            echo '✅ Build successful!'
        }
        failure {
            echo '❌ Build failed!'
        }
        always {
            echo '📦 Pipeline execution finished.'
        }
    }
}


