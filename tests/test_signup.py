import random
import string

import allure

ALERT_FILL_OUT = "Please fill out Username and Password."


def generate_random_username(length=8):
    return "test_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


@allure.epic("Demoblaze")
@allure.feature("Регистрация")
class TestSignUp:

    @allure.story("Успешная регистрация")
    @allure.title("SU01: Успешная регистрация нового пользователя")
    def test_signup_success(self, home_page):
        username = generate_random_username()
        allure.dynamic.parameter("username", username)

        with allure.step("Открыть форму регистрации"):
            signup_page = home_page.go_to_signup()

        with allure.step(f"Зарегистрировать нового пользователя {username}"):
            signup_page.fill_username(username)
            signup_page.fill_password("password123")
            signup_page.click_submit()

        with allure.step("Проверить сообщение об успешной регистрации"):
            alert_text = signup_page.get_alert_text_and_accept()
            assert "sign up successful" in alert_text.lower(), f"Неожиданный текст: {alert_text}"

    @allure.story("Успешная регистрация")
    @allure.title("SU02: Регистрация с цифрами и спецсимволами в пароле")
    def test_signup_with_special_characters(self, home_page):
        username = generate_random_username()

        with allure.step("Открыть форму регистрации"):
            signup_page = home_page.go_to_signup()

        with allure.step("Зарегистрировать пользователя со спецсимволами в пароле"):
            signup_page.fill_username(username)
            signup_page.fill_password("P@ssw0rd_2026!")
            signup_page.click_submit()

        with allure.step("Проверить сообщение об успешной регистрации"):
            alert_text = signup_page.get_alert_text_and_accept()
            assert "sign up successful" in alert_text.lower(), f"Неожиданный текст: {alert_text}"

    @allure.story("Негативные сценарии регистрации")
    @allure.title("SU04: Регистрация без username")
    def test_signup_empty_username(self, home_page):
        with allure.step("Открыть форму регистрации"):
            signup_page = home_page.go_to_signup()

        with allure.step("Оставить username пустым, ввести пароль"):
            signup_page.fill_password("password123")
            signup_page.click_submit()

        with allure.step("Проверить alert о незаполненных полях"):
            alert_text = signup_page.get_alert_text_and_accept()
            assert alert_text == ALERT_FILL_OUT, f"Неожиданный текст alert: {alert_text}"

    @allure.story("Негативные сценарии регистрации")
    @allure.title("SU05: Регистрация без пароля")
    def test_signup_empty_password(self, home_page):
        username = generate_random_username()

        with allure.step("Открыть форму регистрации"):
            signup_page = home_page.go_to_signup()

        with allure.step("Ввести username, оставить пароль пустым"):
            signup_page.fill_username(username)
            signup_page.click_submit()

        with allure.step("Проверить alert о незаполненных полях"):
            alert_text = signup_page.get_alert_text_and_accept()
            assert alert_text == ALERT_FILL_OUT, f"Неожиданный текст alert: {alert_text}"

    @allure.story("Негативные сценарии регистрации")
    @allure.title("SU06: Регистрация без username и пароля")
    def test_signup_empty_both_fields(self, home_page):
        with allure.step("Открыть форму регистрации"):
            signup_page = home_page.go_to_signup()

        with allure.step("Оставить оба поля пустыми и подтвердить"):
            signup_page.click_submit()

        with allure.step("Проверить alert о незаполненных полях"):
            alert_text = signup_page.get_alert_text_and_accept()
            assert alert_text == ALERT_FILL_OUT, f"Неожиданный текст alert: {alert_text}"
