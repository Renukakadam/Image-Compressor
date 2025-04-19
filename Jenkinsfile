pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        PYTHON = '"C:\\Program Files\\Python312\\python.exe"'
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Renukakadam/Image-Compressor.git'
            }
        }

        stage('Set Up Virtual Environment') {
            steps {
                bat """
                    %PYTHON% -m venv %VENV_DIR%
                    call %VENV_DIR%\\Scripts\\activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage('Run Script') {
            steps {
                bat """
                    call %VENV_DIR%\\Scripts\\activate
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
