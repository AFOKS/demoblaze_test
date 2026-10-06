import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils.alerts import accept_alert
from .base_page import BasePage


class LoginPage(BasePage):
    username_input = (By.ID, "loginusername")
    password_input = (By.ID, "loginpassword")
    submit_btn = (By.CSS_SELECTOR, "#logInModal button[onclick='logIn()']")
    welcome_message = (By.ID, "nameofuser")
    logout_btn = (By.ID, "logout2")

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

    @allure.step("Нажать 'Log in'")
    def click_submit(self):
        self.wait.until(EC.element_to_be_clickable(self.submit_btn)).click()

    @allure.step("Получить текст alert и закрыть его")
    def get_alert_text_and_accept(self, timeout: int = 10) -> str:
        return accept_alert(self.driver, timeout)

    @allure.step("Получить приветственное сообщение в хедере")
    def get_welcome_message(self) -> str:
        element = self.wait.until(EC.visibility_of_element_located(self.welcome_message))
        # Текст подставляется после ответа сервера, ждём, пока он появится
        self.wait.until(lambda d: element.text.strip() != "")
        return element.text.strip()

    @allure.step("Выйти из системы")
    def logout(self):
        self.wait.until(EC.element_to_be_clickable(self.logout_btn)).click()
