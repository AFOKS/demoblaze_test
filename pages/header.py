from selenium.webdriver.common.by import By
from .base_page import BasePage

class Header(BasePage):
    LOCATORS = {
        "signup_btn": (By.ID, "signin2"),
        "login_btn": (By.ID, "login2"),
        "cart_btn": (By.CSS_SELECTOR, "a[href='#/cart']"),
        "about_link": (By.CSS_SELECTOR, "a[href='#/about']"),
    }

    def open_signup(self):
        self.click(self.LOCATORS["signup_btn"])

    def open_login(self):
        self.click(self.LOCATORS["login_btn"])

    def open_cart(self):
        self.click(self.LOCATORS["cart_btn"])

    def open_about(self):
        self.click(self.LOCATORS["about_link"])