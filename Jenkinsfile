pipeline {
    agent any

    environment {
        // Define environment variables if needed
        DEPLOY_DIR = "/var/www/image-compressor"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/your-username/image-compressor.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    source venv/bin/activate
                    pytest
                '''
            }
        }

        stage('Build') {
            steps {
                echo 'Building the Image Compressor...'
                // Add any build steps here if applicable
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying to server...'
                // SSH Deploy Example
                sshagent(['deploy-key']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no user@your-server-ip << EOF
                        cd /var/www/image-compressor
                        git pull origin main
                        source venv/bin/activate
                        systemctl restart image-compressor
                        EOF
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
