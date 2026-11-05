pipeline {
    agent any
    environment {
        DOCKER_HUB_REPO    = 'andre1chirkov/ci-cd-practice'
        DOCKER_HUB_CRED_ID = 'docker-hub-credentials'
        IMAGE_TAG          = "${env.BUILD_NUMBER}"
        APP_CONTAINER_NAME = 'ci-cd-practice-app'
        APP_PORT           = '8081'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Lint') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements-dev.txt
                    ruff check app.py
                '''
            }
        }
        stage('Test') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest -v
                '''
            }
        }
        stage('Build') {
            steps {
                sh "docker build -t ${DOCKER_HUB_REPO}:${IMAGE_TAG} -t ${DOCKER_HUB_REPO}:latest ."
            }
        }
        stage('Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: DOCKER_HUB_CRED_ID,
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${DOCKER_HUB_REPO}:${IMAGE_TAG}
                        docker push ${DOCKER_HUB_REPO}:latest
                    '''
                }
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                    docker stop ${APP_CONTAINER_NAME} 2>/dev/null || true
                    docker rm   ${APP_CONTAINER_NAME} 2>/dev/null || true

                    docker run -d \
                        --name ${APP_CONTAINER_NAME} \
                        --restart unless-stopped \
                        -p ${APP_PORT}:8081 \
                        ${DOCKER_HUB_REPO}:${IMAGE_TAG}

                    sleep 3

                    curl -fsS http://localhost:${APP_PORT}/health
                '''
            }
        }
    }
    post {
        success {
            echo "Deployed ${DOCKER_HUB_REPO}:${IMAGE_TAG} on port ${APP_PORT}"
        }
        always {
            sh 'docker logout || true'
            cleanWs()
        }
    }
}