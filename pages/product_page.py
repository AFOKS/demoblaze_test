import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils.alerts import accept_alert
from .base_page import BasePage


class ProductPage(BasePage):
    add_to_cart_btn = (By.XPATH, "//a[contains(text(), 'Add to cart')]")
    product_title = (By.CSS_SELECTOR, "h2.name")

    @allure.step("Нажать 'Add to cart'")
    def click_add_to_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.add_to_cart_btn)).click()

    @allure.step("Добавить товар в корзину")
    def add_to_cart(self) -> str:
        self.click_add_to_cart()
        return accept_alert(self.driver)

    @allure.step("Получить название товара")
    def get_product_title(self) -> str:
        return self.wait.until(
            EC.visibility_of_element_located(self.product_title)
        ).text
