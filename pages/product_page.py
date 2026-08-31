from selenium.webdriver.common.by import By
from .base_page import BasePage

class ProductPage(BasePage):
    LOCATORS = {
        "product_by_name": (By.XPATH, "//a[contains(text(),{})]"),
        "add_to_cart": (By.CSS_SELECTOR, "button[data-qa='addToCart']"),
        "product_title": (By.CSS_SELECTOR, "h2[data-qa='productName']"),
    }

    def open_product(self, product_name):
        # На главной кликаем по продукту
        locator = (By.XPATH, f"//a[contains(text(),'{product_name}')]")
        self.click(locator)

    def add_to_cart(self):
        self.click(self.LOCATORS["add_to_cart"])

    def get_product_title(self):
        return self.find(self.LOCATORS["product_title"]).text