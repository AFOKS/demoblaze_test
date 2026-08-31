from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    LOCATORS = {
        "username": (By.ID, "loginusername"),
        "password": (By.ID, "loginpassword"),
        "submit": (By.CSS_SELECTOR, "button[data-qa='login']"),
        "user_link": (By.CSS_SELECTOR, "a[href='#/index']"),  # после логина появляется имя
    }

    def login(self, username, password):
        self.driver.find_element(*self.LOCATORS["username"]).send_keys(username)
        self.driver.find_element(*self.LOCATORS["password"]).send_keys(password)
        self.click(self.LOCATORS["submit"])

    def is_logged_in(self, username):
        # После успешного логина в хедере появляется ссылка с именем
        user_el = self.driver.find_element(By.CSS_SELECTOR, f"a[href='#/index']")
        return username.lower() in user_el.text.lower()