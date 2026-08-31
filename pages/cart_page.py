from selenium.webdriver.common.by import By
from .base_page import BasePage

class CartPage(BasePage):
    LOCATORS = {
        "cart_items": (By.CSS_SELECTOR, "tr[data-qa='cart-item']"),
        "total": (By.CSS_SELECTOR, "h3[data-qa='cartTotal']"),
        "checkout_btn": (By.CSS_SELECTOR, "button[data-qa='checkout']"),
    }

    def get_items_count(self):
        return len(self.driver.find_elements(*self.LOCATORS["cart_items"]))

    def get_total_text(self):
        return self.find(self.LOCATORS["total"]).text

    def go_to_checkout(self):
        self.click(self.LOCATORS["checkout_btn"])