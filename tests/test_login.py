import pytest
from pages.login_page import LoginPage


@pytest.mark.allure("login")
class TestLogin:
    """Тесты входа пользователя"""

    def test_login_success(self, home_page):
        """LO06: Успешный вход с валидными данными"""
        username = "testuser"
        password = "password123"

        login_page = home_page.go_to_login()
        login_page.login(username, password)
        welcome = login_page.get_welcome_message()

        assert "Welcome" in welcome, f"Ожидалось приветствие, получено: {welcome}"

    def test_login_invalid_username(self, home_page):
        """LO01: Вход с неверным username (негативный тест)"""
        username = "nonexistent_user_xyz"
        password = "password123"

        login_page = home_page.go_to_login()
        login_page.login(username, password)

        # Проверяем, что остались на странице логина
        current_url = login_page.driver.current_url
        assert "index.html" in current_url, "Вход выполнен с неверным username"

    def test_login_invalid_password(self, home_page):
        """LO02: Вход с неверным паролем (негативный тест)"""
        username = "testuser"
        password = "wrong_password_xyz"

        login_page = home_page.go_to_login()
        login_page.login(username, password)

        current_url = login_page.driver.current_url
        assert "index.html" in current_url, "Вход выполнен с неверным паролем"

    def test_login_empty_username(self, home_page):
        """LO04: Вход без username (негативный тест)"""
        username = ""
        password = "password123"

        login_page = home_page.go_to_login()
        login_page.login(username, password)

        current_url = login_page.driver.current_url
        assert "index.html" in current_url, "Вход выполнен с пустым username"

    def test_login_empty_password(self, home_page):
        """LO05: Вход без пароля (негативный тест)"""
        username = "testuser"
        password = ""

        login_page = home_page.go_to_login()
        login_page.login(username, password)

        current_url = login_page.driver.current_url
        assert "index.html" in current_url, "Вход выполнен с пустым паролем"

    def test_login_empty_both_fields(self, home_page):
        """LO05: Вход без username и пароля (негативный тест)"""
        username = ""
        password = ""

        login_page = home_page.go_to_login()
        login_page.login(username, password)

        current_url = login_page.driver.current_url
        assert "index.html" in current_url, "Вход выполнен с пустыми полями"

    def test_logout_success(self, home_page):
        """LO07: Успешный выход из системы"""
        username = "testuser"
        password = "password123"

        # Вход
        login_page = home_page.go_to_login()
        login_page.login(username, password)

        # Проверяем, что вошли
        welcome = login_page.get_welcome_message()
        assert "Welcome" in welcome, "Не удалось войти для теста logout"

        # Выход
        from pages.home_page import HomePage
        home_page_after_login = HomePage(login_page.driver)
        home_page_after_login.click((pytest.By.ID, "log out"))

        # Проверяем, что кнопка Login снова появилась
        assert home_page_after_login.find_element((pytest.By.ID, "login")), "Кнопка Login не найдена после logout"