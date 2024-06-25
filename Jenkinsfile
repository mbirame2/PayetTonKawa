pipeline {
    // agent any
    agent any
    environment {
        DOCKER_IMAGE = 'mbirame2/payetonkawa_client'
        SONARQUBE_URL = 'http://localhost:9000'
        SONARQUBE_TOKEN = credentials('sonarqube-token')
        JAVA_HOME = "/usr/lib/jvm/java-1.17.0-openjdk-amd64"
        SONARQUBE_LOGIN = 'admin'
        SONARQUBE_PASSWORD = 'musulmant'
        DOCKERHUB_USERNAME='mbirame2'
        DOCKERHUB_PASSWORD = 'musulmant2000'
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        //PATH = "${env.JAVA_HOME}/bin:${env.PATH}"
        PATH = "/opt/sonar-scanner/bin:$PATH"
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
                sh './venv/bin/pytest test.py'
            }
        }

        stage('Code Quality Analysis') {
            tools {
                jdk "jdk17" // the name you have given the JDK installation using the JDK manager (Global Tool Configuration)
            }
            steps {
                script {
                    withSonarQubeEnv('SonarQube') {
                        sh "/usr/local/sonar-scanner/bin/sonar-scanner -Dsonar.projectKey=paye_ton_kawa_commande -Dsonar.analysisCache.enabled=false -Dsonar.sources=. -Dsonar.host.url=${SONARQUBE_URL} -Dsonar.login=${env.SONARQUBE_LOGIN} -Dsonar.password=${env.SONARQUBE_PASSWORD} -Dsonar.ws.timeout=120 -Dsonar.java.binaries=**/*.java"
                    }
                }
            } 
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "/usr/local/bin/docker build -t ${DOCKER_IMAGE}:${env.BUILD_ID} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                    //     sh "/usr/local/bin/docker push ${DOCKER_IMAGE}:${env.BUILD_ID}"
                    // }
                    sh "/usr/local/bin/docker login -u ${DOCKERHUB_USERNAME} -p ${DOCKERHUB_PASSWORD}"
                    sh "/usr/local/bin/docker push ${DOCKER_IMAGE}:${env.BUILD_ID}"
                    sh "/usr/local/bin/docker logout"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {                
                    sh "/usr/local/bin/docker pull ${DOCKER_IMAGE}:${env.BUILD_ID}"
                    sh "/usr/local/bin/docker run -d -p 8002:8000 ${DOCKER_IMAGE}:${env.BUILD_ID}"                 
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
