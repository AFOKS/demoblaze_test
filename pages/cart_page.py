import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage
from .checkout_page import CheckoutPage


class CartPage(BasePage):
    LOCATORS = {
        "cart_items": (By.CSS_SELECTOR, "#tbodyid tr"),
        "total": (By.ID, "totalp"),
        "checkout_btn": (By.XPATH, "//button[contains(text(), 'Place Order')]"),
    }

    @allure.step("Получить количество товаров в корзине")
    def get_cart_items_count(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.LOCATORS["cart_items"])
            )
        except TimeoutException:
            return 0
        return len(self.driver.find_elements(*self.LOCATORS["cart_items"]))

    @allure.step("Получить текст суммы корзины")
    def get_total_text(self):
        WebDriverWait(self.driver, 10).until(
            lambda d: self.find(self.LOCATORS["total"]).text.strip() not in ("", "0")
        )
        return self.find(self.LOCATORS["total"]).text.strip()

    @allure.step("Получить сумму корзины числом")
    def get_total(self) -> float:
        text = self.get_total_text()
        try:
            return float(text)
        except (TypeError, ValueError):
            return 0.0

    @allure.step("Удалить первый товар из корзины")
    def remove_first_product(self):
        delete_button = self.find(
            (By.XPATH, "//tbody[@id='tbodyid']//tr[1]//a[text()='Delete']")
        )
        delete_button.click()
        # Дождаться, пока строка реально исчезнет из DOM
        WebDriverWait(self.driver, 5).until(
            EC.staleness_of(delete_button)
        )

    @allure.step("Перейти к оформлению заказа")
    def go_to_checkout(self) -> CheckoutPage:
        self.click(self.LOCATORS["checkout_btn"])
        checkout_page = CheckoutPage(self.driver, self.base_url)
        checkout_page.find(checkout_page.LOCATORS["name"])
        return checkout_page