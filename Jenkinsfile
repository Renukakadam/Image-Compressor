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
                bat """
                "%PYTHON_PATH%" -m venv venv
                call venv\\Scripts\\activate.bat
                pip install --upgrade pip
                pip install -r requirements.txt
                """
            }
        }

        stage('Run Script') {
            steps {
                bat """
                call venv\\Scripts\\activate.bat
                python main.py
                """
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

