pipeline {
    agent any

    tools {
        python 'Python3' // Ensure this is configured in Jenkins global tools
    }

    environment {
        VENV_DIR = 'venv'
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
                sh '''
                    if [ ! -d "$VENV_DIR" ]; then
                        python3 -m venv $VENV_DIR
                    fi
                    source $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Script') {
            steps {
                sh '''
                    source $VENV_DIR/bin/activate
                    python main.py
                '''
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
            echo '🧹 Cleaning up...'
            sh 'deactivate || true' // In case it's active
        }
    }
}

