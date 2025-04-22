pipeline {
    agent any

    stages {
        stage('Checkout SCM') {
            steps {
                // Clone the repository
                checkout scm
                // Store the commit hash
                script {
                    env.CURRENT_COMMIT = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                }
            }
        }

        stage('Check for Changes') {
            steps {
                script {
                    // Get previous successful commit or fallback
                    def previousCommit = env.LAST_SUCCESSFUL_COMMIT ?: sh(script: 'git rev-parse HEAD^', returnStdout: true).trim()
                    env.LAST_SUCCESSFUL_COMMIT = env.CURRENT_COMMIT
                    
                    // Check for changes
                    def changes = sh(script: "git diff --name-only ${previousCommit} ${env.CURRENT_COMMIT}", returnStdout: true).trim()
                    if (changes) {
                        echo "Changes detected:\n${changes}"
                        env.HAS_CHANGES = 'true'
                    } else {
                        echo 'No changes detected.'
                        env.HAS_CHANGES = 'false'
                    }
                }
            }
        }

        stage('Install Dependencies') {
            when {
                expression { env.HAS_CHANGES == 'true' }
            }
            steps {
                // Install Python dependencies
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            when {
                expression { env.HAS_CHANGES == 'true' }
            }
            steps {
                // Run tests using pytest
                bat 'python -m pytest tests/ --junitxml=test-results.xml'
            }
        }
    }

    post {
        always {
            // Publish test results
            junit 'test-results.xml'
            echo 'Pipeline execution finished.'
        }
        success {
            echo 'Build and tests successful!'
        }
        failure {
            echo 'Build failed!'
        }
        cleanup {
            // Clean workspace
            cleanWs()
        }
    }
}
