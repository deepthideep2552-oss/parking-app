// Jenkinsfile - CI/CD pipeline for Parking Slot Booking System
// Works on Windows (bat) and Linux/Mac (sh) Jenkins automatically.

pipeline {
    agent any

    environment {
        IMAGE_NAME     = 'parking-app'
        CONTAINER_NAME = 'parking-app-container'
        APP_PORT       = '5000'
        // Docker Desktop is installed for one Windows user, so docker.exe is not on
        // the PATH of the Jenkins service (LocalSystem). runCmd() adds this folder.
        DOCKER_BIN     = 'C:\\Users\\diisr\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin'
    }

    // Run one build at a time, so two builds never deploy the same container at once.
    options {
        disableConcurrentBuilds()
    }

    // Auto-trigger: Jenkins checks GitHub every 2 minutes for new commits.
    // (If you set up a GitHub webhook, the build starts instantly instead.)
    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Pulling latest code from GitHub...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    runCmd("docker version")
                    runCmd("docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -t ${IMAGE_NAME}:latest .")
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    runCmd("docker run --rm ${IMAGE_NAME}:latest python -m pytest -v")
                }
            }
        }

        stage('Deploy Container') {
            steps {
                script {
                    // Remove old container if it exists (ignore error if not)
                    runCmd("docker rm -f ${CONTAINER_NAME}", true)
                    runCmd("docker run -d --name ${CONTAINER_NAME} -p ${APP_PORT}:5000 ${IMAGE_NAME}:latest")
                }
            }
        }
    }

    post {
        success {
            echo "SUCCESS: App is running at http://localhost:${APP_PORT}"
        }
        failure {
            echo 'FAILED: Check the console output above for errors.'
        }
    }
}

// Helper: use 'bat' on Windows and 'sh' on Linux/Mac
def runCmd(String cmd, boolean ignoreErrors = false) {
    if (isUnix()) {
        return sh(script: cmd, returnStatus: ignoreErrors)
    } else {
        return withEnv(["PATH+DOCKER=${env.DOCKER_BIN}"]) {
            bat(script: cmd, returnStatus: ignoreErrors)
        }
    }
}
