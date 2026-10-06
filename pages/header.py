from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage


class Header(BasePage):
    signup_btn = (By.ID, "signin2")
    login_btn = (By.ID, "login2")
    cart_btn = (By.ID, "cartur")
    about_link = (By.CSS_SELECTOR, "a[data-target='#videoModal']")

    def open_signup(self):
        self.wait.until(EC.element_to_be_clickable(self.signup_btn)).click()

    def open_login(self):
        self.wait.until(EC.element_to_be_clickable(self.login_btn)).click()

    def open_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.cart_btn)).click()

    def open_about(self):
        self.wait.until(EC.element_to_be_clickable(self.about_link)).click()
