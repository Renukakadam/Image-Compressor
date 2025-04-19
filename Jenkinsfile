pipeline {
    agent any

    environment {
        GIT_REPO = 'https://github.com/Renukakadam/Image-Compressor.git'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                script {
                    // Checkout the code from the git repository
                    git url: GIT_REPO, branch: 'main'
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                bat 'pip install -r requirements.txt' // Assuming you're using pip for Python dependencies
            }
        }

        stage('Linting') {
            steps {
                echo 'Running linting...'
                bat 'flake8 .' // Replace with the correct linter command if needed
            }
        }

        stage('Build') {
            steps {
                echo 'Building the project...'
                bat 'python setup.py build' // Replace with your actual build command
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                bat 'pytest tests/' // Replace with your actual test command
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            // Add any cleanup steps here, such as deleting temporary files or logs.
        }
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}

