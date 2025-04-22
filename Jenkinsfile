pipeline {
    agent any

    stages {
        stage('Checkout SCM') {
            steps {
                // Clone the repository
                checkout scm
                // Store the commit hash using SCM metadata
                script {
                    env.CURRENT_COMMIT = env.GIT_COMMIT
                }
            }
        }

        stage('Check for Changes') {
            steps {
                script {
                    // Get previous successful commit or fallback
                    def previousCommit = env.LAST_SUCCESSFUL_COMMIT ?: bat(script: '"C:\\Program Files\\Git\\bin\\git.exe" rev-parse HEAD^', returnStdout: true).trim()
                    env.LAST_SUCCESSFUL_COMMIT = env.CURRENT_COMMIT
                    
                    // Check for changes
                    def changes = bat(script: '"C:\\Program Files\\Git\\bin\\git.exe" diff --name-only %LAST_SUCCESSFUL_COMMIT% %CURRENT_COMMIT%', returnStdout: true).trim()
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
                allOf {
                    expression { env.HAS_CHANGES == 'true' }
                    expression { fileExists('requirements.txt') }
                }
            }
            steps {
                // Install Python dependencies
                bat 'python -m pip install pytest'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            when {
                expression { env.HAS_CHANGES == 'true' }
            }
            steps {
                script {
                    try {
                        // Run tests using pytest, if tests exist
                        bat 'python -m pytest tests/ --junitxml=test-results.xml'
                    } catch (Exception e) {
                        echo "Warning: Tests failed or not found. Continuing pipeline. Error: ${e}"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }
    }

    post {
        always {
            // Publish test results if they exist
            script {
                if (fileExists('test-results.xml')) {
                    junit 'test-results.xml'
                } else {
                    echo 'No test results found, skipping JUnit publishing.'
                }
            }
            echo 'Pipeline execution finished.'
        }
        success {
            echo 'Build and tests successful!'
        }
        unstable {
            echo 'Tests failed, but pipeline continued.'
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

