import allure


@allure.epic("Demoblaze")
@allure.feature("Корзина")
class TestCart:

    @allure.story("Добавление товаров")
    @allure.title("C01: Добавление одного товара в корзину")
    def test_add_single_product_to_cart(self, home_page):
        with allure.step("Выбрать товар"):
            product_page = home_page.select_product(0)

        with allure.step("Добавить товар в корзину"):
            product_page.add_to_cart()

        with allure.step("Проверить количество товаров в корзине"):
            cart_page = home_page.go_to_cart()
            items_count = cart_page.get_cart_items_count()
            assert items_count >= 1, f"Ожидался хотя бы 1 товар в корзине, найдено: {items_count}"

    @allure.story("Добавление товаров")
    @allure.title("C02: Добавление нескольких товаров в корзину")
    def test_add_multiple_products_to_cart(self, home_page):
        with allure.step("Добавить первый товар"):
            product_page_1 = home_page.select_product(0)
            product_page_1.add_to_cart()

        with allure.step("Вернуться на главную страницу"):
            home_page.open()

        with allure.step("Добавить второй товар"):
            product_page_2 = home_page.select_product(1)
            product_page_2.add_to_cart()

        with allure.step("Проверить количество товаров в корзине"):
            cart_page = home_page.go_to_cart()
            items_count = cart_page.get_cart_items_count()
            assert items_count >= 2, f"Ожидалось хотя бы 2 товара в корзине, найдено: {items_count}"

    @allure.story("Удаление товаров")
    @allure.title("C03: Удаление товара из корзины")
    def test_remove_product_from_cart(self, home_page):
        with allure.step("Добавить товар в корзину"):
            product_page = home_page.select_product(0)
            product_page.add_to_cart()

        with allure.step("Открыть корзину и запомнить количество товаров"):
            cart_page = home_page.go_to_cart()
            initial_count = cart_page.get_cart_items_count()

        with allure.step("Удалить первый товар"):
            cart_page.remove_first_product()

        with allure.step("Проверить, что количество товаров уменьшилось"):
            final_count = cart_page.get_cart_items_count()
            assert final_count < initial_count, "Товар не был удалён из корзины"

    @allure.story("Расчёт суммы")
    @allure.title("C04: Проверка расчёта общей суммы в корзине")
    def test_cart_total_calculation(self, home_page):
        with allure.step("Добавить товар в корзину"):
            product_page = home_page.select_product(0)
            product_page.add_to_cart()

        with allure.step("Проверить сумму в корзине"):
            cart_page = home_page.go_to_cart()
            total = cart_page.get_total()
            assert total > 0, f"Ожидалась сумма больше 0, получено: {total}"