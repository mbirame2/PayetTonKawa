pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'mbirame2/payeTonKawa-produit'
        SONARQUBE_URL = 'http://localhost:9000'
        SONARQUBE_TOKEN = credentials('sonarqube-token')
    }

    stages {
        stage('Checkout') {
            steps {
                git url: "${env.GIT_URL}", branch: "${env.BRANCH_NAME}"
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    // Ensure Python 3 is installed
                    sh '''
                        if ! command -v python3 &> /dev/null
                        then
                            echo "Python 3 could not be found. Installing..."
                            sudo apt update
                            sudo apt install -y python3 python3-venv
                        fi
                    '''
                    
                    // Create and activate a virtual environment
                    sh '''
                        python3 -m venv venv
                        source venv/bin/activate
                    '''
                }
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install -r requirements.txt'
                sh './venv/bin/pytest tests/'
            }
        }

        stage('Code Quality Analysis') {
            steps {
                script {
                    withSonarQubeEnv('SonarQube') {
                        sh "./venv/bin/sonar-scanner -Dsonar.projectKey=your-project-key-${env.BRANCH_NAME} -Dsonar.sources=. -Dsonar.host.url=${SONARQUBE_URL} -Dsonar.login=${SONARQUBE_TOKEN}"
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${env.BUILD_ID}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        docker.image("${DOCKER_IMAGE}:${env.BUILD_ID}").push()
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    docker.withRegistry('', 'dockerhub-credentials') {
                        sh 'docker pull ${DOCKER_IMAGE}:${env.BUILD_ID}'
                        sh 'docker run -d -p 80:80 ${DOCKER_IMAGE}:${env.BUILD_ID}'
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
