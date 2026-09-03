from pages.login_page import LoginPage
from selenium.webdriver.common.by import By

VALID_USERNAME = "test.test123"
VALID_PASSWORD = "123456"


class TestLogin:
    """Тесты входа пользователя"""

    def test_login_success(self, home_page):
        """LO06: Успешный вход с валидными данными"""
        login_page = home_page.go_to_login()
        login_page.login(VALID_USERNAME, VALID_PASSWORD)

        alert_text = login_page.get_alert_text_and_accept()
        assert alert_text is None, f"Логин не должен показывать alert, получено: {alert_text}"

        welcome = login_page.get_welcome_message()
        assert "Welcome" in welcome, f"Ожидалось приветствие, получено: {welcome}"

    def test_login_invalid_username(self, home_page):
        """LO01: Вход с неверным username (негативный тест)"""
        login_page = home_page.go_to_login()
        login_page.login("nonexistent_user_xyz", VALID_PASSWORD)

        alert_text = login_page.get_alert_text_and_accept()
        assert alert_text is not None, "Ожидался alert об ошибке входа"

    def test_login_invalid_password(self, home_page):
        """LO02: Вход с неверным паролем (негативный тест)"""
        login_page = home_page.go_to_login()
        login_page.login(VALID_USERNAME, "wrong_password_xyz")

        alert_text = login_page.get_alert_text_and_accept()
        assert alert_text is not None, "Ожидался alert об ошибке входа"

    def test_login_empty_username(self, home_page):
        """LO04: Вход без username (негативный тест)"""
        login_page = home_page.go_to_login()
        login_page.login("", VALID_PASSWORD)

        alert_text = login_page.get_alert_text_and_accept()
        assert alert_text is not None, "Ожидался alert о незаполненных полях"

    def test_login_empty_password(self, home_page):
        """LO05: Вход без пароля (негативный тест)"""
        login_page = home_page.go_to_login()
        login_page.login(VALID_USERNAME, "")

        alert_text = login_page.get_alert_text_and_accept()
        assert alert_text is not None, "Ожидался alert о незаполненных полях"

    def test_login_empty_both_fields(self, home_page):
        """LO05: Вход без username и пароля (негативный тест)"""
        login_page = home_page.go_to_login()
        login_page.login("", "")

        alert_text = login_page.get_alert_text_and_accept()
        assert alert_text is not None, "Ожидался alert о незаполненных полях"

    def test_logout_success(self, home_page):
        """LO07: Успешный выход из системы"""
        login_page = home_page.go_to_login()
        login_page.login(VALID_USERNAME, VALID_PASSWORD)

        welcome = login_page.get_welcome_message()
        assert "Welcome" in welcome, "Не удалось войти для теста logout"

        login_page.logout()

        login_btn = login_page.wait.until(
            lambda d: d.find_element(By.ID, "login2")
        )
        assert login_btn.is_displayed(), "Кнопка Login не найдена после logout"