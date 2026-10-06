import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base_page import WebPage
from .cart_page import CartPage
from .login_page import LoginPage
from .product_page import ProductPage
from .signup_page import SignupPage


class HomePage(WebPage):
    path = ""

    product_cards = (By.CSS_SELECTOR, "#tbodyid .card h4 a")
    cart_link = (By.ID, "cartur")
    login_btn = (By.ID, "login2")
    signup_btn = (By.ID, "signin2")

    @allure.step("Выбрать товар с индексом {index}")
    def select_product(self, index: int) -> ProductPage:
        products = self.wait.until(
            EC.presence_of_all_elements_located(self.product_cards)
        )
        products[index].click()
        return ProductPage(self.driver)

    @allure.step("Выбрать товар '{name}'")
    def select_product_by_name(self, name: str) -> ProductPage:
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, name))).click()
        return ProductPage(self.driver)

    @allure.step("Перейти в корзину")
    def go_to_cart(self) -> CartPage:
        self.wait.until(EC.element_to_be_clickable(self.cart_link)).click()
        cart_page = CartPage(self.driver, self.base_url)
        self.wait.until(EC.presence_of_element_located(cart_page.total))
        return cart_page

    @allure.step("Открыть форму входа")
    def go_to_login(self) -> LoginPage:
        self.wait.until(EC.element_to_be_clickable(self.login_btn)).click()
        login_page = LoginPage(self.driver)
        self.wait.until(EC.visibility_of_element_located(login_page.username_input))
        return login_page

    @allure.step("Открыть форму регистрации")
    def go_to_signup(self) -> SignupPage:
        self.wait.until(EC.element_to_be_clickable(self.signup_btn)).click()
        signup_page = SignupPage(self.driver)
        self.wait.until(EC.visibility_of_element_located(signup_page.username_input))
        return signup_page
