from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage


class LoginPage(BasePage):
    LOCATORS = {
        "username": (By.ID, "loginusername"),
        "password": (By.ID, "loginpassword"),
        "submit": (By.CSS_SELECTOR, "#logInModal button[onclick='logIn()']"),
        "welcome_message": (By.ID, "nameofuser"),
        "logout_btn": (By.ID, "logout2"),
    }

    def login(self, username: str, password: str):
        self.driver.find_element(*self.LOCATORS["username"]).send_keys(username)
        self.driver.find_element(*self.LOCATORS["password"]).send_keys(password)
        self.click(self.LOCATORS["submit"])

    def get_alert_text_and_accept(self, timeout: int = 10):
        """Ждём alert (в т.ч. с задержкой ответа сервера). None — если alert не появился."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            text = alert.text
            alert.accept()
            return text
        except TimeoutException:
            return None

    def get_welcome_message(self, timeout: int = 10) -> str:
        """Ждём, пока JS реально впишет текст приветствия, а не просто появления элемента."""
        def _welcome_text(driver):
            text = driver.find_element(*self.LOCATORS["welcome_message"]).text.strip()
            return text if text else False

        return WebDriverWait(self.driver, timeout).until(_welcome_text)

    def logout(self):
        self.click(self.LOCATORS["logout_btn"])