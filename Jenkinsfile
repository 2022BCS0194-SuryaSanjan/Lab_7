pipeline {
    agent any

    environment {
        IMAGE = "sanjan2022bcs0194/wine-ml-model:latest"
        CONTAINER = "wine-test"
        // Using 127.0.0.1 is more reliable than 'localhost' in many Jenkins environments
        BASE_URL = "http://127.0.0.1:8000"
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
                // Using explicit port mapping (-p) to bridge the host and container
                sh 'docker run -d -p 8000:8000 --name $CONTAINER $IMAGE'
            }
        }

        stage('Wait for API') {
            steps {
                sh '''
                count=1
                while [ $count -le 12 ]
                do
                  # Check the docs endpoint for a 200 OK response
                  if curl -s -f http://127.0.0.1:8000/docs; then
                    echo "API is up!"
                    exit 0
                  fi
                  echo "Attempt $count: API not ready yet..."
                  sleep 5
                  count=$((count + 1))
                done
        
                echo "FAILED: Printing logs for wine-test to find the error:"
                docker logs wine-test
                exit 1
                '''
            }
        }

        stage('Inference Test') {
            steps {
                sh '''
                # Converting JSON to Query Parameters for the GET request
                QUERY=$(jq -r 'to_entries|map("\\(.key)=\\(.value)")|join("&")' valid_input.json)

                echo "Sending Request to: $BASE_URL/predict?$QUERY"
                
                curl -s "$BASE_URL/predict?$QUERY" > output.json
                '''

                sh 'cat output.json'

                // Validates if the output contains the expected response key
                sh 'grep -q "wine_quality" output.json'
            }
        }
    }

    post {
        always {
            // Clean up the container to free up port 8000 for the next build
            sh 'docker rm -f $CONTAINER || true'
        }
    }
}
