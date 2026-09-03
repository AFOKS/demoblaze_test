import allure
from selenium.webdriver.common.by import By

VALID_USERNAME = "testuser"
VALID_PASSWORD = "password123"


@allure.epic("Demoblaze")
@allure.feature("Авторизация")
class TestLogin:

    @allure.story("Успешный вход")
    @allure.title("LO06: Успешный вход с валидными данными")
    def test_login_success(self, home_page):
        with allure.step("Открыть форму логина"):
            login_page = home_page.go_to_login()

        with allure.step("Ввести валидные логин и пароль"):
            login_page.login(VALID_USERNAME, VALID_PASSWORD)

        with allure.step("Проверить, что alert не появился"):
            alert_text = login_page.get_alert_text_and_accept()
            assert alert_text is None, f"Логин не должен показывать alert, получено: {alert_text}"

        with allure.step("Проверить приветственное сообщение"):
            welcome = login_page.get_welcome_message()
            assert "Welcome" in welcome, f"Ожидалось приветствие, получено: {welcome}"

    @allure.story("Негативные сценарии входа")
    @allure.title("LO01: Вход с неверным username")
    def test_login_invalid_username(self, home_page):
        with allure.step("Открыть форму логина"):
            login_page = home_page.go_to_login()

        with allure.step("Ввести несуществующий username"):
            login_page.login("nonexistent_user_xyz", VALID_PASSWORD)

        with allure.step("Проверить, что появился alert с ошибкой"):
            alert_text = login_page.get_alert_text_and_accept()
            assert alert_text is not None, "Ожидался alert об ошибке входа"

    @allure.story("Негативные сценарии входа")
    @allure.title("LO02: Вход с неверным паролем")
    def test_login_invalid_password(self, home_page):
        with allure.step("Открыть форму логина"):
            login_page = home_page.go_to_login()

        with allure.step("Ввести неверный пароль"):
            login_page.login(VALID_USERNAME, "wrong_password_xyz")

        with allure.step("Проверить, что появился alert с ошибкой"):
            alert_text = login_page.get_alert_text_and_accept()
            assert alert_text is not None, "Ожидался alert об ошибке входа"

    @allure.story("Негативные сценарии входа")
    @allure.title("LO04: Вход без username")
    def test_login_empty_username(self, home_page):
        with allure.step("Открыть форму логина"):
            login_page = home_page.go_to_login()

        with allure.step("Оставить username пустым"):
            login_page.login("", VALID_PASSWORD)

        with allure.step("Проверить, что появился alert о незаполненных полях"):
            alert_text = login_page.get_alert_text_and_accept()
            assert alert_text is not None, "Ожидался alert о незаполненных полях"

    @allure.story("Негативные сценарии входа")
    @allure.title("LO05: Вход без пароля")
    def test_login_empty_password(self, home_page):
        with allure.step("Открыть форму логина"):
            login_page = home_page.go_to_login()

        with allure.step("Оставить пароль пустым"):
            login_page.login(VALID_USERNAME, "")

        with allure.step("Проверить, что появился alert о незаполненных полях"):
            alert_text = login_page.get_alert_text_and_accept()
            assert alert_text is not None, "Ожидался alert о незаполненных полях"

    @allure.story("Негативные сценарии входа")
    @allure.title("LO05: Вход без username и пароля")
    def test_login_empty_both_fields(self, home_page):
        with allure.step("Открыть форму логина"):
            login_page = home_page.go_to_login()

        with allure.step("Оставить оба поля пустыми"):
            login_page.login("", "")

        with allure.step("Проверить, что появился alert о незаполненных полях"):
            alert_text = login_page.get_alert_text_and_accept()
            assert alert_text is not None, "Ожидался alert о незаполненных полях"

    @allure.story("Выход из системы")
    @allure.title("LO07: Успешный выход из системы")
    def test_logout_success(self, home_page):
        with allure.step("Войти в систему"):
            login_page = home_page.go_to_login()
            login_page.login(VALID_USERNAME, VALID_PASSWORD)
            welcome = login_page.get_welcome_message()
            assert "Welcome" in welcome, "Не удалось войти для теста logout"

        with allure.step("Выйти из системы"):
            login_page.logout()

        with allure.step("Проверить, что кнопка Login снова видна"):
            login_btn = login_page.wait.until(lambda d: d.find_element(By.ID, "login2"))
            assert login_btn.is_displayed(), "Кнопка Login не найдена после logout"