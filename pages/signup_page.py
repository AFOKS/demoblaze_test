from selenium.webdriver.common.by import By
from .base_page import BasePage

class SignupPage(BasePage):
    LOCATORS = {
        "username": (By.ID, "sign-username"),
        "password": (By.ID, "sign-password"),
        "submit": (By.CSS_SELECTOR, "button[data-qa='sign-up']"),
        "message": (By.CSS_SELECTOR, ".sweet-alert .sweet-alert-success, .sweet-alert p"),
    }

    def signup(self, username, password):
        self.driver.find_element(*self.LOCATORS["username"]).send_keys(username)
        self.driver.find_element(*self.LOCATORS["password"]).send_keys(password)
        self.click(self.LOCATORS["submit"])

    def get_success_message(self):
        return self.find(self.LOCATORS["message"]).text.strip()