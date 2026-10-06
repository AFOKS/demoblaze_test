import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils.alerts import accept_alert
from .base_page import BasePage


class SignupPage(BasePage):
    username_input = (By.ID, "sign-username")
    password_input = (By.ID, "sign-password")
    submit_btn = (By.CSS_SELECTOR, "#signInModal button[onclick='register()']")

    @allure.step("Ввести логин '{username}'")
    def fill_username(self, username: str):
        field = self.wait.until(EC.visibility_of_element_located(self.username_input))
        field.clear()
        field.send_keys(username)

    @allure.step("Ввести пароль")
    def fill_password(self, password: str):
        field = self.wait.until(EC.visibility_of_element_located(self.password_input))
        field.clear()
        field.send_keys(password)

    @allure.step("Нажать 'Sign up'")
    def click_submit(self):
        self.wait.until(EC.element_to_be_clickable(self.submit_btn)).click()

    @allure.step("Получить текст alert и закрыть его")
    def get_alert_text_and_accept(self, timeout: int = 10) -> str:
        return accept_alert(self.driver, timeout)
