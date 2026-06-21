pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-southeast-1'
        AWS_ACCOUNT_ID = '154931139523'
        EKS_CLUSTER_NAME = 'cms-eks-tf'

        BACKEND_REPO = 'cms-backend-tf'
        FRONTEND_REPO = 'cms-frontend-tf'

        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Login to ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region $AWS_REGION \
                | docker login --username AWS --password-stdin $ECR_REGISTRY
                '''
            }
        }

        stage('Build Backend Image') {
            steps {
                sh '''
                docker build -t $BACKEND_REPO:latest ./backend
                docker tag $BACKEND_REPO:latest $ECR_REGISTRY/$BACKEND_REPO:latest
                '''
            }
        }

        stage('Build Frontend Image') {
            steps {
                sh '''
                docker build -t $FRONTEND_REPO:latest ./frontend
                docker tag $FRONTEND_REPO:latest $ECR_REGISTRY/$FRONTEND_REPO:latest
                '''
            }
        }

        stage('Push Images to ECR') {
            steps {
                sh '''
                docker push $ECR_REGISTRY/$BACKEND_REPO:latest
                docker push $ECR_REGISTRY/$FRONTEND_REPO:latest
                '''
            }
        }

        stage('Update Kubeconfig') {
            steps {
                sh '''
                aws eks update-kubeconfig \
                  --region $AWS_REGION \
                  --name $EKS_CLUSTER_NAME
                '''
            }
        }

        stage('Deploy to EKS') {
            steps {
                sh '''
                kubectl rollout restart deployment cms-backend -n cms
                kubectl rollout restart deployment cms-frontend -n cms

                kubectl rollout status deployment cms-backend -n cms
                kubectl rollout status deployment cms-frontend -n cms
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully.'
        }

        failure {
            echo 'CI/CD pipeline failed. Check Jenkins console logs.'
        }
    }
}
