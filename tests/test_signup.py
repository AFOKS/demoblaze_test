import random
import string
from pages.signup_page import SignupPage


def generate_random_username(length=8):
    return "test_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


class TestSignUp:
    """Тесты регистрации пользователя"""

    def test_signup_success(self, home_page):
        """SU01: Успешная регистрация нового пользователя"""
        signup_page = home_page.go_to_signup()
        signup_page.sign_up(generate_random_username(), "password123")

        alert_text = signup_page.get_alert_text_and_accept()
        assert alert_text is not None, "Ожидался alert об успешной регистрации"
        assert "sign up successful" in alert_text.lower(), f"Неожиданный текст: {alert_text}"

    def test_signup_with_special_characters(self, home_page):
        """SU02: Регистрация с цифрами и спецсимволами в пароле"""
        signup_page = home_page.go_to_signup()
        signup_page.sign_up(generate_random_username(), "P@ssw0rd_2026!")

        alert_text = signup_page.get_alert_text_and_accept()
        assert alert_text is not None, "Ожидался alert об успешной регистрации"
        assert "sign up successful" in alert_text.lower(), "Регистрация с спецсимволами не удалась"

    def test_signup_empty_username(self, home_page):
        """SU04: Регистрация без username (негативный тест)"""
        signup_page = home_page.go_to_signup()
        signup_page.sign_up("", "password123")

        alert_text = signup_page.get_alert_text_and_accept()
        assert alert_text is not None, "Ожидался alert о незаполненных полях"

    def test_signup_empty_password(self, home_page):
        """SU05: Регистрация без пароля (негативный тест)"""
        signup_page = home_page.go_to_signup()
        signup_page.sign_up(generate_random_username(), "")

        alert_text = signup_page.get_alert_text_and_accept()
        assert alert_text is not None, "Ожидался alert о незаполненных полях"

    def test_signup_empty_both_fields(self, home_page):
        """SU06: Регистрация без username и пароля (негативный тест)"""
        signup_page = home_page.go_to_signup()
        signup_page.sign_up("", "")

        alert_text = signup_page.get_alert_text_and_accept()
        assert alert_text is not None, "Ожидался alert о незаполненных полях"