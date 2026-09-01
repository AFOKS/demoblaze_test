from selenium.webdriver.common.by import By
from .base_page import BasePage


class CartPage(BasePage):

    LOCATORS = {
        "cart_items": (By.CSS_SELECTOR, "#tbodyid tr"),
        "total": (By.ID, "totalp"),
        "checkout_btn": (
            By.XPATH,
            "//button[contains(text(), 'Place Order')]"
        ),
    }

    def get_cart_items_count(self):
        return len(
            self.driver.find_elements(
                *self.LOCATORS["cart_items"]
            )
        )

    def get_total_text(self):
        return self.find(
            (By.ID, "totalp")
        ).text

    def remove_first_product(self):
        delete_button = self.find(
            (
                By.XPATH,
                "//tbody[@id='tbodyid']//tr[1]//a[text()='Delete']"
            )
        )
        delete_button.click()

    def go_to_checkout(self):
        self.click(
            self.LOCATORS["checkout_btn"]
        )