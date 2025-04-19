pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                sh 'npm install'
            }
        }

        stage('Linting') {
            steps {
                echo 'Running lint checks...'
                sh 'npm run lint || echo "Linting errors found, but continuing..."'
            }
        }

        stage('Build') {
            steps {
                echo 'Building the project...'
                sh 'npm run build'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                sh 'npm test'
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed!'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
    }
}

