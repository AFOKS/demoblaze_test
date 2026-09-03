import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .base_page import BasePage


class ProductPage(BasePage):
    LOCATORS = {
        "add_to_cart": (By.XPATH, "//a[contains(text(), 'Add to cart')]"),
        "product_title": (By.CSS_SELECTOR, "h2.name"),
    }

    @allure.step("Открыть товар '{product_name}'")
    def open_product(self, product_name):
        locator = (By.XPATH, f"//a[contains(text(), '{product_name}')]")
        self.click(locator)

    @allure.step("Добавить товар в корзину")
    def add_to_cart(self):
        self.click(self.LOCATORS["add_to_cart"])
        alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert.accept()

    @allure.step("Получить название товара")
    def get_product_title(self):
        return self.find(self.LOCATORS["product_title"]).text