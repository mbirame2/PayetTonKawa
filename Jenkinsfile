pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'mbirame2/payeTonKawa-produit'
        SONARQUBE_URL = 'http://192.168.1.71:9000'
        SONARQUBE_TOKEN = credentials('sonarqube-token')
        JAVA_HOME = "/usr/lib/jvm/java-1.17.0-openjdk-amd64"
        //PATH = "${env.JAVA_HOME}/bin:${env.PATH}"
        PATH = "/opt/sonar-scanner-cli-6.0.0.4432-linux/bin:$PATH"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: "${env.GIT_URL}", branch: "${env.BRANCH_NAME}"
            }
        }

        stage('Check Java Version') {
            steps {
                sh 'java -version'
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
                            apt update
                            apt install -y python3 python3-venv
                        fi
                    '''
                    
                    // Create and activate a virtual environment
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                    '''
                }
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'python3 -m venv venv'
                sh "./venv/bin/pip install pytest==6.2.4"
                sh "./venv/bin/pip install requests==2.25.1"
                sh "./venv/bin/pip install fastapi"
                sh './venv/bin/pytest testu.py'
            }
        }

        stage('Code Quality Analysis') {
            tools {
                jdk "jdk17" // the name you have given the JDK installation using the JDK manager (Global Tool Configuration)
            }
            steps {
                script {
                    withSonarQubeEnv('SonarQube') {
                        sh "sonar-scanner -Dsonar.projectKey=your-project-key-${env.BRANCH_NAME} -Dsonar.sources=. -Dsonar.host.url=${SONARQUBE_URL} -Dsonar.login=${SONARQUBE_TOKEN}"
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
