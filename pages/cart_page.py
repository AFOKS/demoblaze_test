import logging

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base_page import WebPage
from .checkout_page import CheckoutPage

logger = logging.getLogger(__name__)


class CartPage(WebPage):
    path = "cart.html"

    cart_rows = (By.CSS_SELECTOR, "#tbodyid tr")
    total = (By.ID, "totalp")
    first_delete_link = (By.XPATH, "//tbody[@id='tbodyid']//tr[1]//a[text()='Delete']")
    place_order_btn = (By.XPATH, "//button[contains(text(), 'Place Order')]")

    @allure.step("Дождаться появления товаров в корзине")
    def wait_for_items(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.cart_rows))
        except TimeoutException:
            logger.warning(
                "Товары в корзине не появились за %s с", self.timeout
            )

    @allure.step("Получить количество товаров в корзине")
    def get_cart_items_count(self) -> int:
        return len(self.driver.find_elements(*self.cart_rows))

    @allure.step("Получить текст суммы корзины")
    def get_total_text(self) -> str:
        return self.driver.find_element(*self.total).text.strip()

    @allure.step("Получить сумму корзины числом")
    def get_total(self) -> float | None:
        text = self.get_total_text()
        return float(text) if text else None

    @allure.step("Удалить первый товар из корзины")
    def remove_first_product(self):
        delete_link = self.wait.until(
            EC.element_to_be_clickable(self.first_delete_link)
        )
        delete_link.click()
        # Дождаться, пока строка реально исчезнет из DOM
        self.wait.until(EC.staleness_of(delete_link))

    @allure.step("Перейти к оформлению заказа")
    def go_to_checkout(self) -> CheckoutPage:
        self.wait.until(EC.element_to_be_clickable(self.place_order_btn)).click()
        checkout_page = CheckoutPage(self.driver)
        self.wait.until(EC.visibility_of_element_located(checkout_page.name_input))
        return checkout_page
