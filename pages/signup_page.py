import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage


class SignupPage(BasePage):
    LOCATORS = {
        "username": (By.ID, "sign-username"),
        "password": (By.ID, "sign-password"),
        "submit": (By.CSS_SELECTOR, "#signInModal button[onclick='register()']"),
    }

    @allure.step("Зарегистрировать пользователя '{username}'")
    def sign_up(self, username: str, password: str):
        self.driver.find_element(*self.LOCATORS["username"]).send_keys(username)
        self.driver.find_element(*self.LOCATORS["password"]).send_keys(password)
        self.click(self.LOCATORS["submit"])

    @allure.step("Получить текст alert и закрыть его")
    def get_alert_text_and_accept(self, timeout: int = 10):
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            text = alert.text
            alert.accept()
            return text
        except TimeoutException:
            return None