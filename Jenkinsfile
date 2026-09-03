pipeline {
    agent any

    parameters {
        choice(
            name: 'BROWSER',
            choices: ['chrome', 'firefox'],
            description: 'Браузер для запуска тестов'
        )
        string(
            name: 'BROWSER_VERSION',
            defaultValue: '120.0',
            description: 'Версия браузера в Selenoid'
        )
        string(
            name: 'RESOLUTION',
            defaultValue: '1920x1080',
            description: 'Разрешение экрана браузера'
        )
        string(
            name: 'SITE_URL',
            defaultValue: 'https://www.demoblaze.com/',
            description: 'URL тестируемого сайта'
        )
        string(
            name: 'TEST_PATH',
            defaultValue: 'tests/',
            description: 'Путь до тестов, которые нужно запустить'
        )
    }

    environment {
        SELENOID_LOGIN    = credentials('selenoid-login')     // Secret text credential
        SELENOID_PASSWORD = credentials('selenoid-password')  // Secret text credential
        SELENOID_URL      = credentials('selenoid-host-url')  // Secret text credential
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest ${TEST_PATH} \
                        --browser=${BROWSER} \
                        --browser-version=${BROWSER_VERSION} \
                        --resolution=${RESOLUTION} \
                        --site-url=${SITE_URL} \
                        --alluredir=allure-results \
                        -v
                '''
            }
        }
    }

    post {
        always {
            allure includeProperties: false,
                   jdk: '',
                   results: [[path: 'allure-results']]
        }
        failure {
            echo 'Тесты упали — детали смотрите в Allure-отчёте job\'а.'
        }
    }
}