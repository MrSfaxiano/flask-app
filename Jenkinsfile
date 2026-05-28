pipeline {
    agent any

    environment {
        IMAGE_NAME = "MrSfaxiano/flask-app"
        IMAGE_TAG  = "${env.GIT_COMMIT[0..6]}"
        REGISTRY_CREDENTIALS = 'dockerhub-credentials'
    }

    options {
        timestamps()
        ansiColor('xterm')
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Checking out commit ${env.GIT_COMMIT} on branch ${env.GIT_BRANCH}"
                checkout scm
            }
        }

        stage('Lint') {
            steps {
                echo 'Running flake8 linter...'
                sh '''
                    docker run --rm \
                        -v $(pwd):/app \
                        -w /app \
                        python:3.12-slim \
                        sh -c "pip install flake8 --quiet && python -m flake8 app/"
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running unit tests...'
                sh '''
                    docker run --rm \
                        -v $(pwd):/app \
                        -w /app \
                        python:3.12-slim \
                        sh -c "pip install -r requirements-dev.txt --quiet && python -m pytest tests/ -v --junit-xml=test-results.xml"
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Build') {
            steps {
                echo "Building Docker image ${env.IMAGE_NAME}:${env.IMAGE_TAG}..."
                sh "docker build -t ${env.IMAGE_NAME}:${env.IMAGE_TAG} ."
                sh "docker tag ${env.IMAGE_NAME}:${env.IMAGE_TAG} ${env.IMAGE_NAME}:latest"
            }
        }

        stage('Push') {
            steps {
                echo 'Pushing image to Docker Hub...'
                withCredentials([usernamePassword(
                    credentialsId: env.REGISTRY_CREDENTIALS,
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying to staging...'
                sh '''
                    docker stop flask-app-staging 2>/dev/null || true
                    docker rm flask-app-staging 2>/dev/null || true
                    docker run -d \
                        --name flask-app-staging \
                        --network jenkins-cicd_cicd \
                        -p 5000:5000 \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                '''
                echo "App deployed at http://localhost:5000/health"
            }
        }

    }

    post {
        success {
            echo "Pipeline succeeded. Image: ${env.IMAGE_NAME}:${env.IMAGE_TAG}"
        }
        failure {
            echo "Pipeline failed. Check logs above."
        }
        always {
            sh 'docker logout || true'
            cleanWs()
        }
    }
}

# retrigger2
