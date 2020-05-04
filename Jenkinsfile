pipeline {
    agent any
    stages {
        stage('Deploy') {
            steps {
                sh "sed -i 's/localhost/${env.DOMAIN}/g' variables.env"
                sh "cat variables.env"
                sh "./scripts/deploy.sh"
            }
        }
    }
}