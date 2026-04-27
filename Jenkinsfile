pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
    }

    environment {
        IMAGE_NAME   = "karthikeyajeshwanth/fraud-detection-model"
        FULL_IMAGE   = "${IMAGE_NAME}:${BUILD_NUMBER}"
        APP_NAME     = "fraud-api"
        PROJECT_ID   = "model-journal-431911-h3"
        CLUSTER_NAME = "fraud-cluster"
        ZONE         = "asia-south1-a"

        CLOUD_SDK_PATH  = "C:\\Users\\abcom\\AppData\\Local\\Google\\Cloud SDK\\google-cloud-sdk\\bin"
        KUBECONFIG_PATH = "${WORKSPACE}\\.kube\\config"
    }

    stages {

        // 🔽 1
        stage('1. Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/reddydilip145-hub/ml-recommendation-system-mlops.git'
            }
        }

        // 🔽 2
        stage('2. Debug Environment') {
            steps {
                bat """
                @echo off
                set PATH=%PATH%;%CLOUD_SDK_PATH%

                echo BUILD NUMBER: %BUILD_NUMBER%
                docker --version
                kubectl version --client
                gcloud --version
                """
            }
        }

        // 🔽 3
        stage('3. Build Docker Image') {
            steps {
                bat "docker build --no-cache -t %FULL_IMAGE% ."
            }
        }

        // 🔽 4
        stage('4. Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat """
                    @echo off
                    docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                    docker push %FULL_IMAGE%
                    """
                }
            }
        }

        // 🔽 5
        stage('5. Prepare Kubeconfig') {
            steps {
                bat """
                @echo off
                if not exist "%WORKSPACE%\\.kube" mkdir "%WORKSPACE%\\.kube"
                """
            }
        }

        // 🔽 6
        stage('6. Authenticate with GCP') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GCP_KEY')]) {
                    bat """
                    @echo off
                    set PATH=%PATH%;%CLOUD_SDK_PATH%

                    gcloud auth activate-service-account --key-file="%GCP_KEY%"
                    gcloud config set project %PROJECT_ID%
                    """
                }
            }
        }

        // 🔽 7
        stage('7. Connect to GKE Cluster') {
            steps {
                bat """
                @echo off
                set PATH=%PATH%;%CLOUD_SDK_PATH%
                set KUBECONFIG=%KUBECONFIG_PATH%

                gcloud container clusters get-credentials %CLUSTER_NAME% ^
                    --zone %ZONE% ^
                    --project %PROJECT_ID%

                kubectl config current-context
                kubectl get nodes
                """
            }
        }

        // 🔽 8
        stage('8. Deploy Application') {
            steps {
                bat """
                @echo off
                set PATH=%PATH%;%CLOUD_SDK_PATH%
                set KUBECONFIG=%KUBECONFIG_PATH%

                kubectl apply -f service.yaml
                kubectl set image deployment/%APP_NAME% %APP_NAME%=%FULL_IMAGE%
                kubectl rollout status deployment/%APP_NAME% --timeout=180s
                """
            }
        }

        // 🔥 9 (FINAL FIXED STAGE)
        stage('9. Verify & Health Check') {
            steps {
                script {
                    retry(5) {

                        sleep 30

                        def svc_ip = bat(
                            script: """
                            @echo off
                            set PATH=%PATH%;${CLOUD_SDK_PATH}
                            set KUBECONFIG=${KUBECONFIG_PATH}

                            kubectl get svc fraud-api-service -o jsonpath={.status.loadBalancer.ingress[0].ip}
                            """,
                            returnStdout: true
                        ).trim()

                        // 🔥 CLEAN OUTPUT
                        svc_ip = svc_ip.tokenize().last()

                        echo "Service IP: ${svc_ip}"

                        if (!svc_ip) {
                            error "LoadBalancer IP not ready"
                        }

                        def status = bat(
                            script: "@echo off & curl -s -o NUL -w %%{http_code} http://${svc_ip}/health",
                            returnStdout: true
                        ).trim()

                        echo "Health Status: ${status}"

                        if (status != "200") {
                            error "Health check failed"
                        }
                    }
                }
            }
        }
    }

    post {

        success {
            echo "🎉 SUCCESS: CI/CD pipeline completed successfully"
        }

        failure {
            echo "❌ FAILURE: Rolling back deployment"

            bat """
            @echo off
            set PATH=%PATH%;%CLOUD_SDK_PATH%
            set KUBECONFIG=%KUBECONFIG_PATH%

            kubectl rollout undo deployment/%APP_NAME%
            kubectl rollout status deployment/%APP_NAME%
            """
        }
    }
}