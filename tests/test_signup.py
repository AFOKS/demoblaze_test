import pytest
import random
import string
from pages.signup_page import SignUpPage


def generate_random_username(length=8):
    """Генерация случайного username"""
    return "test_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


@pytest.mark.allure("signup")
class TestSignUp:
    """Тесты регистрации пользователя"""

    def test_signup_success(self, home_page):
        """SU01: Успешная регистрация нового пользователя"""
        username = generate_random_username()
        password = "password123"

        signup_page = home_page.go_to_signup()
        signup_page.sign_up(username, password)
        message = signup_page.get_success_message()

        assert "Sign up successful" in message, f"Ожидалось сообщение об успехе, получено: {message}"

    def test_signup_with_special_characters(self, home_page):
        """SU02: Регистрация с цифрами и спецсимволами в пароле"""
        username = generate_random_username()
        password = "P@ssw0rd_2026!"

        signup_page = home_page.go_to_signup()
        signup_page.sign_up(username, password)
        message = signup_page.get_success_message()

        assert "Sign up successful" in message, "Регистрация с спецсимволами не удалась"

    def test_signup_empty_username(self, home_page):
        """SU04: Регистрация без username (негативный тест)"""
        username = ""
        password = "password123"

        signup_page = home_page.go_to_signup()
        signup_page.sign_up(username, password)

        # Проверяем, что форма не отправилась или появилась ошибка
        current_url = signup_page.driver.current_url
        assert "index.html" in current_url, "Регистрация прошла с пустым username"

    def test_signup_empty_password(self, home_page):
        """SU05: Регистрация без пароля (негативный тест)"""
        username = generate_random_username()
        password = ""

        signup_page = home_page.go_to_signup()
        signup_page.sign_up(username, password)

        current_url = signup_page.driver.current_url
        assert "index.html" in current_url, "Регистрация прошла с пустым паролем"

    def test_signup_empty_both_fields(self, home_page):
        """SU06: Регистрация без username и пароля (негативный тест)"""
        username = ""
        password = ""

        signup_page = home_page.go_to_signup()
        signup_page.sign_up(username, password)

        current_url = signup_page.driver.current_url
        assert "index.html" in current_url, "Регистрация прошла с пустыми полями"