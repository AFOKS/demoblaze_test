from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .base_page import BasePage
from .product_page import ProductPage
from .cart_page import CartPage
from .login_page import LoginPage
from .signup_page import SignupPage


class HomePage(BasePage):
    LOCATORS = {
        "product_cards": (By.CSS_SELECTOR, "#tbodyid .card h4 a"),
        "cart_link": (By.CSS_SELECTOR, "#cartur"),
        "login_btn": (By.ID, "login2"),
        "signup_btn": (By.ID, "signin2"),
    }

    def __init__(self, driver, base_url: str):
        super().__init__(driver, base_url)

    def open(self):
        self.driver.get(self.base_url)
        return self

    def select_product(self, index: int) -> ProductPage:
        # Отдельный, более щедрый wait именно для AJAX-подгрузки карточек
        products = WebDriverWait(self.driver, 15).until(
            EC.presence_of_all_elements_located(self.LOCATORS["product_cards"])
        )

        if not products:
            raise RuntimeError("На главной странице не найдены товары")

        if index < 0 or index >= len(products):
            raise IndexError(
                f"Индекс товара {index} вне диапазона [0, {len(products) - 1}]"
            )

        products[index].click()
        return ProductPage(self.driver, self.base_url)

    def go_to_cart(self) -> CartPage:
        self.click(self.LOCATORS["cart_link"])
        cart_page = CartPage(self.driver, self.base_url)
        # ждём, пока корзина реально отрисуется (total всегда есть в DOM)
        cart_page.find(cart_page.LOCATORS["total"])
        return cart_page

    def go_to_login(self) -> LoginPage:
        self.click(self.LOCATORS["login_btn"])
        login_page = LoginPage(self.driver, self.base_url)
        login_page.find(login_page.LOCATORS["username"])
        return login_page

    def go_to_signup(self) -> SignupPage:
        self.click(self.LOCATORS["signup_btn"])
        signup_page = SignupPage(self.driver, self.base_url)
        signup_page.find(signup_page.LOCATORS["username"])
        return signup_page