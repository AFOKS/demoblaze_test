import pytest


@pytest.mark.allure("checkout")
class TestCheckout:
    """Тесты оформления заказа"""

    def test_checkout_success(self, home_page):
        """CH01: Успешное оформление заказа"""
        # Добавляем товар
        product_page = home_page.select_product(0)
        product_page.add_to_cart()

        # Переходим в корзину и на checkout
        cart_page = home_page.go_to_cart()
        checkout_page = cart_page.go_to_checkout()

        # Заполняем форму
        checkout_page.fill_checkout_form(
            name="John Doe",
            country="Latvia",
            city="Riga",
            card="4111111111111111",
            month="12",
            year="2026"
        )
        checkout_page.purchase()

        # Проверяем успех
        message = checkout_page.get_success_message()
        assert "Thank you for your purchase!" in message, f"Ожидалось подтверждение заказа, получено: {message}"

    def test_checkout_with_empty_fields(self, home_page):
        """CH02: Оформление заказа с пустыми полями (негативный тест)"""
        # Добавляем товар
        product_page = home_page.select_product(0)
        product_page.add_to_cart()

        # Переходим в корзину и на checkout
        cart_page = home_page.go_to_cart()
        checkout_page = cart_page.go_to_checkout()

        # Пытаемся оформить с пустыми полями
        checkout_page.fill_checkout_form(
            name="",
            country="",
            city="",
            card="",
            month="",
            year=""
        )
        checkout_page.purchase()

        # Проверяем, что заказ не оформился (нет сообщения об успехе)
        from selenium.common.exceptions import TimeoutException
        try:
            message = checkout_page.get_success_message()
            assert "Thank you for your purchase!" not in message, "Заказ оформился с пустыми полями"
        except TimeoutException:
            # Ожидаемое поведение - сообщение не появилось
            pass

    def test_checkout_invalid_card(self, home_page):
        """CH03: Оформление заказа с невалидной картой (негативный тест)"""
        # Добавляем товар
        product_page = home_page.select_product(0)
        product_page.add_to_cart()

        # Переходим в корзину и на checkout
        cart_page = home_page.go_to_cart()
        checkout_page = cart_page.go_to_checkout()

        # Заполняем форму с невалидной картой
        checkout_page.fill_checkout_form(
            name="John Doe",
            country="Latvia",
            city="Riga",
            card="1234567890123456",  # Невалидный номер
            month="13",  # Невалидный месяц
            year="2020"  # Прошедший год
        )
        checkout_page.purchase()

        # Проверяем, что заказ не оформился
        from selenium.common.exceptions import TimeoutException
        try:
            message = checkout_page.get_success_message()
            assert "Thank you for your purchase!" not in message, "Заказ оформился с невалидной картой"
        except TimeoutException:
            # Ожидаемое поведение - сообщение не появилось
            pass