import allure
import pytest
from selenium.common.exceptions import TimeoutException


@allure.epic("Demoblaze")
@allure.feature("Оформление заказа")
class TestCheckout:

    @allure.story("Успешное оформление")
    @allure.title("CH01: Успешное оформление заказа")
    def test_checkout_success(self, home_page):
        with allure.step("Добавить товар в корзину"):
            product_page = home_page.select_product(0)
            product_page.add_to_cart()

        with allure.step("Перейти в корзину и открыть форму заказа"):
            cart_page = home_page.go_to_cart()
            checkout_page = cart_page.go_to_checkout()

        with allure.step("Заполнить форму заказа валидными данными"):
            checkout_page.fill_checkout_form(
                name="John Doe", country="Latvia", city="Riga",
                card="4111111111111111", month="12", year="2026"
            )

        with allure.step("Оформить заказ"):
            checkout_page.purchase()

        with allure.step("Проверить сообщение об успешном заказе"):
            message = checkout_page.get_success_message()
            assert "Thank you for your purchase!" in message, f"Ожидалось подтверждение заказа, получено: {message}"

    @allure.story("Негативные сценарии оформления")
    @allure.title("CH02: Оформление заказа с пустыми полями")
    def test_checkout_with_empty_fields(self, home_page):
        with allure.step("Добавить товар в корзину"):
            product_page = home_page.select_product(0)
            product_page.add_to_cart()

        with allure.step("Перейти в корзину и открыть форму заказа"):
            cart_page = home_page.go_to_cart()
            checkout_page = cart_page.go_to_checkout()

        with allure.step("Оставить все поля пустыми и попытаться оформить заказ"):
            checkout_page.fill_checkout_form(name="", country="", city="", card="", month="", year="")
            checkout_page.purchase()

        with allure.step("Проверить, что заказ не оформился"):
            try:
                message = checkout_page.get_success_message(timeout=5)
                assert "Thank you for your purchase!" not in message, "Заказ оформился с пустыми полями"
            except TimeoutException:
                pass  # ожидаемое поведение

    @allure.story("Негативные сценарии оформления")
    @allure.title("CH03: Оформление заказа с невалидной картой")
    @pytest.mark.xfail(
        reason="Demoblaze не валидирует формат карты/срок действия — заказ всё равно оформляется"
    )
    def test_checkout_invalid_card(self, home_page):
        with allure.step("Добавить товар в корзину"):
            product_page = home_page.select_product(0)
            product_page.add_to_cart()

        with allure.step("Перейти в корзину и открыть форму заказа"):
            cart_page = home_page.go_to_cart()
            checkout_page = cart_page.go_to_checkout()

        with allure.step("Заполнить форму невалидными данными карты"):
            checkout_page.fill_checkout_form(
                name="John Doe", country="Latvia", city="Riga",
                card="1234567890123456", month="13", year="2020"
            )
            checkout_page.purchase()

        with allure.step("Проверить, что заказ не оформился"):
            try:
                message = checkout_page.get_success_message(timeout=5)
                assert "Thank you for your purchase!" not in message, "Заказ оформился с невалидной картой"
            except TimeoutException:
                pass