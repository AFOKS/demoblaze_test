pipeline {
    agent {
        label 'python'
    }

    parameters {
        choice(
            name: 'BROWSER',
            choices: ['chrome', 'firefox'],
            description: 'Браузер для запуска тестов'
        )

        string(
            name: 'BROWSER_VERSION',
            defaultValue: '148.0',
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
            description: 'Путь до тестов'
        )
    }

    stages {

        stage('Setup Python') {
            steps {
                sh '''
                    python3 --version
                    python3 -m venv .venv

                    . .venv/bin/activate

                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Prepare .env') {
            steps {
                sh '''
                    cat > .env << 'EOF'
SELENOID_LOGIN=ваш_логин
SELENOID_PASSWORD=ваш_пароль
SELENOID_URL=ваш_хост_selenoid
EOF
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                    . .venv/bin/activate

                    python -m pytest ${TEST_PATH} \
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
            script {
                if (fileExists('allure-results')) {
                    allure(
                        includeProperties: false,
                        jdk: '',
                        results: [[path: 'allure-results']]
                    )
                } else {
                    echo 'allure-results не найден — тесты не запускались или не создали результаты.'
                }
            }
        }

        failure {
            echo 'Сборка завершилась с ошибкой. Проверь Console Output.'
        }
    }
}