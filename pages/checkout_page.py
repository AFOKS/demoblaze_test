import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils.alerts import accept_alert
from .base_page import BasePage


class CheckoutPage(BasePage):
    name_input = (By.ID, "name")
    country_input = (By.ID, "country")
    city_input = (By.ID, "city")
    card_input = (By.ID, "card")
    month_input = (By.ID, "month")
    year_input = (By.ID, "year")
    purchase_btn = (By.XPATH, "//button[contains(text(), 'Purchase')]")
    success_message = (By.CSS_SELECTOR, ".sweet-alert h2")

    @allure.step("Ввести имя '{name}'")
    def fill_name(self, name: str):
        field = self.wait.until(EC.visibility_of_element_located(self.name_input))
        field.clear()
        field.send_keys(name)

    @allure.step("Ввести страну '{country}'")
    def fill_country(self, country: str):
        field = self.wait.until(EC.visibility_of_element_located(self.country_input))
        field.clear()
        field.send_keys(country)

    @allure.step("Ввести город '{city}'")
    def fill_city(self, city: str):
        field = self.wait.until(EC.visibility_of_element_located(self.city_input))
        field.clear()
        field.send_keys(city)

    @allure.step("Ввести номер карты '{card}'")
    def fill_card(self, card: str):
        field = self.wait.until(EC.visibility_of_element_located(self.card_input))
        field.clear()
        field.send_keys(card)

    @allure.step("Ввести месяц '{month}'")
    def fill_month(self, month: str):
        field = self.wait.until(EC.visibility_of_element_located(self.month_input))
        field.clear()
        field.send_keys(month)

    @allure.step("Ввести год '{year}'")
    def fill_year(self, year: str):
        field = self.wait.until(EC.visibility_of_element_located(self.year_input))
        field.clear()
        field.send_keys(year)

    @allure.step("Нажать 'Purchase'")
    def click_purchase(self):
        self.wait.until(EC.element_to_be_clickable(self.purchase_btn)).click()

    @allure.step("Получить текст alert и закрыть его")
    def get_alert_text_and_accept(self, timeout: int = 5) -> str:
        return accept_alert(self.driver, timeout)

    @allure.step("Получить сообщение об успешном заказе")
    def get_success_message(self) -> str:
        return self.wait.until(
            EC.visibility_of_element_located(self.success_message)
        ).text.strip()
