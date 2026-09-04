import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage


class CheckoutPage(BasePage):
    LOCATORS = {
        "name": (By.ID, "name"),
        "country": (By.ID, "country"),
        "city": (By.ID, "city"),
        "card": (By.ID, "card"),
        "month": (By.ID, "month"),
        "year": (By.ID, "year"),
        "purchase_btn": (By.XPATH, "//button[contains(text(), 'Purchase')]"),
        "success_message": (By.CSS_SELECTOR, ".sweet-alert h2"),
    }

    @allure.step("Заполнить форму заказа")
    def fill_checkout_form(self, name, country, city, card, month, year):
        values = {
            "name": name, "country": country, "city": city,
            "card": card, "month": month, "year": year,
        }
        for field, value in values.items():
            el = self.wait.until(EC.visibility_of_element_located(self.LOCATORS[field]))
            el.clear()
            el.send_keys(value)

    @allure.step("Нажать 'Purchase'")
    def purchase(self):
        self.click(self.LOCATORS["purchase_btn"])
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            self.driver.switch_to.alert.accept()
        except TimeoutException:
            pass

    @allure.step("Получить сообщение об успешном заказе")
    def get_success_message(self, timeout: int = 10) -> str:
        message_el = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.LOCATORS["success_message"])
        )
        return message_el.text.strip()