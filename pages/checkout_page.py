from selenium.webdriver.common.by import By
from .base_page import BasePage

class CheckoutPage(BasePage):
    LOCATORS = {
        "name": (By.ID, "name"),
        "country": (By.ID, "country"),
        "city": (By.ID, "city"),
        "card": (By.ID, "card"),
        "month": (By.ID, "month"),
        "year": (By.ID, "year"),
        "purchase_btn": (By.CSS_SELECTOR, "button[data-qa='purchase']"),
        "success_message": (By.CSS_SELECTOR, ".sweet-alert .sweet-alert-success, .sweet-alert p"),
    }

    def fill_checkout(self, name, country, city, card, month, year):
        fields = {
            "name": name,
            "country": country,
            "city": city,
            "card": card,
            "month": month,
            "year": year,
        }
        for key, value in fields.items():
            self.driver.find_element(*self.LOCATORS[key]).send_keys(value)

    def purchase(self):
        self.click(self.LOCATORS["purchase_btn"])

    def get_success_message(self):
        return self.find(self.LOCATORS["success_message"]).text.strip()