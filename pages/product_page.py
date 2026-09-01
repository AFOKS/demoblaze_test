from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage


class ProductPage(BasePage):

    LOCATORS = {
        "product_by_name": (
            By.XPATH,
            "//a[contains(text(), '{}')]"
        ),

        "add_to_cart": (
            By.XPATH,
            "//a[contains(text(), 'Add to cart')]"
        ),

        "product_title": (
            By.CSS_SELECTOR,
            "h2.name"
        ),
    }

    def open_product(self, product_name):
        locator = (
            By.XPATH,
            f"//a[contains(text(), '{product_name}')]"
        )
        self.click(locator)

    def add_to_cart(self):
        self.click(self.LOCATORS["add_to_cart"])

        # DemoBlaze показывает JavaScript alert
        # после добавления товара
        alert = WebDriverWait(
            self.driver,
            5
        ).until(EC.alert_is_present())

        alert.accept()

    def get_product_title(self):
        return self.find(
            self.LOCATORS["product_title"]
        ).text

