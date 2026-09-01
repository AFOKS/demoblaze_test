from selenium.webdriver.common.by import By
from .base_page import BasePage
from .product_page import ProductPage
from .cart_page import CartPage


class HomePage(BasePage):
    """
    Главная страница https://www.demoblaze.com/
    """

    LOCATORS = {
        "product_cards": (By.CSS_SELECTOR, "#tbodyid .card h4 a"),
        "cart_link": (By.CSS_SELECTOR, "#cartur"),
    }

    def __init__(self, driver, base_url: str):
        super().__init__(driver, base_url)

    def open(self):
        self.driver.get(self.base_url)
        return self

    def select_product(self, index: int) -> ProductPage:
        products = self.driver.find_elements(
            *self.LOCATORS["product_cards"]
        )

        if not products:
            raise RuntimeError(
                "На главной странице не найдены товары"
            )

        if index < 0 or index >= len(products):
            raise IndexError(
                f"Индекс товара {index} вне диапазона "
                f"[0, {len(products) - 1}]"
            )

        products[index].click()

        return ProductPage(
            self.driver,
            self.base_url
        )

    def go_to_cart(self) -> CartPage:
        self.click(self.LOCATORS["cart_link"])
        return CartPage(
            self.driver,
            self.base_url
        )