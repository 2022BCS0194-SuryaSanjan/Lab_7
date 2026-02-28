pipeline {
    agent any

    environment {
        IMAGE = "sanjan2022bcs0194/wine-ml-model:v2"
        CONTAINER = "wine-api"
        BASE_URL = "http://host.docker.internal:8000"
    }

    stages {

        stage('Cleanup Old Container') {
            steps {
                sh 'docker rm -f $CONTAINER || true'
            }
        }

        stage('Pull Docker Image') {
            steps {
                sh 'docker pull $IMAGE'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d -p 8000:8000 --name $CONTAINER $IMAGE'
            }
        }

        stage('Wait for API') {
            steps {
                sh '''
                for i in {1..12}
                do
                  sleep 5
                  curl -f $BASE_URL/docs && exit 0
                done
                echo "API not ready"
                exit 1
                '''
            }
        }

        stage('Install jq') {
            steps {
                sh '''
                apt-get update
                apt-get install -y jq
                '''
            }
        }

        stage('Inference Test') {
            steps {
                sh '''
                QUERY=$(jq -r 'to_entries|map("\\(.key)=\\(.value)")|join("&")' valid_input.json)

                curl "$BASE_URL/predict?$QUERY" > output.json
                '''

                sh 'cat output.json'

                // ✅ This decides SUCCESS / FAILURE
                sh 'grep -q wine_quality output.json'
            }
        }
    }

    post {
        always {
            sh 'docker rm -f $CONTAINER || true'
        }
    }
}
