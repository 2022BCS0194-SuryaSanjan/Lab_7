pipeline {
    agent any

    environment {
        IMAGE = "sanjan2022bcs0194/wine-ml-model:latest"
        CONTAINER = "wine-api"
        // Changed to localhost because we will use --network host
        BASE_URL = "http://localhost:8000"
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
                // Added --network host so Jenkins can reach it via localhost:8000
                sh 'docker run -d --network host --name $CONTAINER $IMAGE'
            }
        }

        stage('Wait for API') {
            steps {
                sh '''
                for i in {1..12}
                do
                  echo "Checking API attempt $i..."
                  if curl -s -f $BASE_URL/docs; then
                    echo "API is up!"
                    exit 0
                  fi
                  sleep 5
                done
                echo "API not ready"
                exit 1
                '''
            }
        }

        stage('Inference Test') {
            steps {
                sh '''
                # Converting JSON to Query Parameters
                QUERY=$(jq -r 'to_entries|map("\\(.key)=\\(.value)")|join("&")' valid_input.json)

                echo "Sending Request to: $BASE_URL/predict?$QUERY"
                
                curl -s "$BASE_URL/predict?$QUERY" > output.json
                '''

                sh 'cat output.json'

                // ✅ Validates if the output contains the expected key
                sh 'grep -q "wine_quality" output.json'
            }
        }
    }

    post {
        always {
            // Clean up the host network port after the test
            sh 'docker rm -f $CONTAINER || true'
        }
    }
}
