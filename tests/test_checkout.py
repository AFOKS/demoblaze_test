import allure
import pytest


@pytest.fixture
def checkout_page(home_page):
    with allure.step("Добавить товар в корзину"):
        home_page.select_product(0).add_to_cart()

    with allure.step("Перейти в корзину и открыть форму заказа"):
        return home_page.go_to_cart().go_to_checkout()


def fill_checkout_form(page, name, country, city, card, month, year):
    """Шаги заполнения формы: порядок и набор полей решает тест."""
    page.fill_name(name)
    page.fill_country(country)
    page.fill_city(city)
    page.fill_card(card)
    page.fill_month(month)
    page.fill_year(year)


@allure.epic("Demoblaze")
@allure.feature("Оформление заказа")
class TestCheckout:

    @allure.story("Успешное оформление")
    @allure.title("CH01: Успешное оформление заказа")
    def test_checkout_success(self, checkout_page):
        with allure.step("Заполнить форму заказа валидными данными"):
            fill_checkout_form(
                checkout_page,
                name="John Doe", country="Latvia", city="Riga",
                card="4111111111111111", month="12", year="2026",
            )

        with allure.step("Оформить заказ"):
            checkout_page.click_purchase()

        with allure.step("Проверить сообщение об успешном заказе"):
            message = checkout_page.get_success_message()
            assert "Thank you for your purchase!" in message, (
                f"Ожидалось подтверждение заказа, получено: {message}"
            )

    @allure.story("Негативные сценарии оформления")
    @allure.title("CH02: Оформление заказа с пустыми полями")
    def test_checkout_with_empty_fields(self, checkout_page):
        with allure.step("Оставить все поля пустыми и нажать Purchase"):
            checkout_page.click_purchase()

        with allure.step("Проверить alert о незаполненных полях"):
            alert_text = checkout_page.get_alert_text_and_accept()
            assert alert_text == "Please fill out Name and Creditcard.", (
                f"Неожиданный текст alert: {alert_text}"
            )

    @allure.story("Негативные сценарии оформления")
    @allure.title("CH03: Оформление заказа с невалидной картой")
    @pytest.mark.xfail(
        strict=True,
        reason="Demoblaze не валидирует формат карты/срок действия — заказ всё равно оформляется",
    )
    def test_checkout_invalid_card(self, checkout_page):
        with allure.step("Заполнить форму невалидными данными карты"):
            fill_checkout_form(
                checkout_page,
                name="John Doe", country="Latvia", city="Riga",
                card="1234567890123456", month="13", year="2020",
            )

        with allure.step("Нажать Purchase"):
            checkout_page.click_purchase()

        with allure.step("Проверить, что форма отклонена с alert об ошибке"):
            alert_text = checkout_page.get_alert_text_and_accept()
            assert alert_text, "Ожидался alert об ошибке валидации карты"
