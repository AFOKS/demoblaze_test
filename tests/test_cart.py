import pytest


class TestCart:
    """Тесты корзины"""

    def test_add_single_product_to_cart(self, home_page):
        """C01: Добавление одного товара в корзину"""
        product_page = home_page.select_product(0)
        product_page.add_to_cart()

        cart_page = home_page.go_to_cart()
        items_count = cart_page.get_cart_items_count()

        assert items_count >= 1, f"Ожидался хотя бы 1 товар в корзине, найдено: {items_count}"

    def test_add_multiple_products_to_cart(self, home_page):
        """C02: Добавление нескольких товаров в корзину"""
        # Добавляем первый товар
        product_page_1 = home_page.select_product(0)
        product_page_1.add_to_cart()

        # Возвращаемся на главную
        home_page.open()

        # Добавляем второй товар
        product_page_2 = home_page.select_product(1)
        product_page_2.add_to_cart()

        # Проверяем корзину
        cart_page = home_page.go_to_cart()
        items_count = cart_page.get_cart_items_count()

        assert items_count >= 2, f"Ожидалось хотя бы 2 товара в корзине, найдено: {items_count}"

    def test_remove_product_from_cart(self, home_page):
        """C03: Удаление товара из корзины"""
        product_page = home_page.select_product(0)
        product_page.add_to_cart()

        cart_page = home_page.go_to_cart()
        initial_count = cart_page.get_cart_items_count()

        cart_page.remove_first_product()

        final_count = cart_page.get_cart_items_count()

        assert final_count < initial_count, (
            "Товар не был удалён из корзины"
        )

    def test_cart_total_calculation(self, home_page):
        """C04: Проверка расчёта общей суммы в корзине"""
        product_page = home_page.select_product(0)
        product_page.add_to_cart()

        cart_page = home_page.go_to_cart()

        total = cart_page.get_total()

        assert total > 0, (
            f"Ожидалась сумма больше 0, получено: {total}"
        )