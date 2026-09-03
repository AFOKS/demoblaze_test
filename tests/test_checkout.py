import pytest
from selenium.common.exceptions import TimeoutException


class TestCheckout:
    """Тесты оформления заказа"""

    def test_checkout_success(self, home_page):
        """CH01: Успешное оформление заказа"""
        product_page = home_page.select_product(0)
        product_page.add_to_cart()

        cart_page = home_page.go_to_cart()
        checkout_page = cart_page.go_to_checkout()

        checkout_page.fill_checkout_form(
            name="John Doe",
            country="Latvia",
            city="Riga",
            card="4111111111111111",
            month="12",
            year="2026"
        )
        checkout_page.purchase()

        message = checkout_page.get_success_message()
        assert "Thank you for your purchase!" in message, f"Ожидалось подтверждение заказа, получено: {message}"

    def test_checkout_with_empty_fields(self, home_page):
        """CH02: Оформление заказа с пустыми полями (негативный тест)"""
        product_page = home_page.select_product(0)
        product_page.add_to_cart()

        cart_page = home_page.go_to_cart()
        checkout_page = cart_page.go_to_checkout()

        checkout_page.fill_checkout_form(
            name="", country="", city="", card="", month="", year=""
        )
        checkout_page.purchase()

        try:
            message = checkout_page.get_success_message(timeout=5)
            assert "Thank you for your purchase!" not in message, "Заказ оформился с пустыми полями"
        except TimeoutException:
            # Ожидаемое поведение — сообщение об успехе не появилось
            pass

    @pytest.mark.xfail(
        reason="Demoblaze не валидирует формат карты/срок действия — заказ всё равно оформляется"
    )
    def test_checkout_invalid_card(self, home_page):
        """CH03: Оформление заказа с невалидной картой (негативный тест)"""
        product_page = home_page.select_product(0)
        product_page.add_to_cart()

        cart_page = home_page.go_to_cart()
        checkout_page = cart_page.go_to_checkout()

        checkout_page.fill_checkout_form(
            name="John Doe",
            country="Latvia",
            city="Riga",
            card="1234567890123456",
            month="13",
            year="2020"
        )
        checkout_page.purchase()

        try:
            message = checkout_page.get_success_message(timeout=5)
            assert "Thank you for your purchase!" not in message, "Заказ оформился с невалидной картой"
        except TimeoutException:
            pass