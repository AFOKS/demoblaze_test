import allure

ALERT_USER_NOT_EXIST = "User does not exist."
ALERT_WRONG_PASSWORD = "Wrong password."
ALERT_FILL_OUT = "Please fill out Username and Password."


@allure.epic("Demoblaze")
@allure.feature("Авторизация")
class TestLogin:

    @allure.story("Успешный вход")
    @allure.title("LO06: Успешный вход с валидными данными")
    def test_login_success(self, home_page, valid_username, valid_password):
        with allure.step("Открыть форму логина"):
            login_page = home_page.go_to_login()

        with allure.step("Ввести валидные логин и пароль и подтвердить"):
            login_page.fill_username(valid_username)
            login_page.fill_password(valid_password)
            login_page.click_submit()

        with allure.step("Проверить приветственное сообщение"):
            welcome = login_page.get_welcome_message()
            assert "Welcome" in welcome, f"Ожидалось приветствие, получено: {welcome}"

    @allure.story("Негативные сценарии входа")
    @allure.title("LO01: Вход с неверным username")
    def test_login_invalid_username(self, home_page, valid_password):
        with allure.step("Открыть форму логина"):
            login_page = home_page.go_to_login()

        with allure.step("Ввести несуществующий username"):
            login_page.fill_username("nonexistent_user_xyz")
            login_page.fill_password(valid_password)
            login_page.click_submit()

        with allure.step("Проверить alert с ошибкой"):
            alert_text = login_page.get_alert_text_and_accept()
            assert alert_text == ALERT_USER_NOT_EXIST, f"Неожиданный текст alert: {alert_text}"

    @allure.story("Негативные сценарии входа")
    @allure.title("LO02: Вход с неверным паролем")
    def test_login_invalid_password(self, home_page, valid_username):
        with allure.step("Открыть форму логина"):
            login_page = home_page.go_to_login()

        with allure.step("Ввести неверный пароль"):
            login_page.fill_username(valid_username)
            login_page.fill_password("wrong_password_xyz")
            login_page.click_submit()

        with allure.step("Проверить alert с ошибкой"):
            alert_text = login_page.get_alert_text_and_accept()
            assert alert_text == ALERT_WRONG_PASSWORD, f"Неожиданный текст alert: {alert_text}"

    @allure.story("Негативные сценарии входа")
    @allure.title("LO04: Вход без username")
    def test_login_empty_username(self, home_page, valid_password):
        with allure.step("Открыть форму логина"):
            login_page = home_page.go_to_login()

        with allure.step("Оставить username пустым, ввести пароль"):
            login_page.fill_password(valid_password)
            login_page.click_submit()

        with allure.step("Проверить alert о незаполненных полях"):
            alert_text = login_page.get_alert_text_and_accept()
            assert alert_text == ALERT_FILL_OUT, f"Неожиданный текст alert: {alert_text}"

    @allure.story("Негативные сценарии входа")
    @allure.title("LO05: Вход без пароля")
    def test_login_empty_password(self, home_page, valid_username):
        with allure.step("Открыть форму логина"):
            login_page = home_page.go_to_login()

        with allure.step("Ввести username, оставить пароль пустым"):
            login_page.fill_username(valid_username)
            login_page.click_submit()

        with allure.step("Проверить alert о незаполненных полях"):
            alert_text = login_page.get_alert_text_and_accept()
            assert alert_text == ALERT_FILL_OUT, f"Неожиданный текст alert: {alert_text}"

    @allure.story("Негативные сценарии входа")
    @allure.title("LO05: Вход без username и пароля")
    def test_login_empty_both_fields(self, home_page):
        with allure.step("Открыть форму логина"):
            login_page = home_page.go_to_login()

        with allure.step("Оставить оба поля пустыми и подтвердить"):
            login_page.click_submit()

        with allure.step("Проверить alert о незаполненных полях"):
            alert_text = login_page.get_alert_text_and_accept()
            assert alert_text == ALERT_FILL_OUT, f"Неожиданный текст alert: {alert_text}"

    @allure.story("Выход из системы")
    @allure.title("LO07: Успешный выход из системы")
    def test_logout_success(self, home_page, header, valid_username, valid_password):
        with allure.step("Войти в систему"):
            login_page = home_page.go_to_login()
            login_page.fill_username(valid_username)
            login_page.fill_password(valid_password)
            login_page.click_submit()
            welcome = login_page.get_welcome_message()
            assert "Welcome" in welcome, "Не удалось войти для теста logout"

        with allure.step("Выйти из системы"):
            login_page.logout()

        with allure.step("Проверить, что кнопка Login снова видна"):
            assert header.is_login_visible(), "Кнопка Login не найдена после logout"
