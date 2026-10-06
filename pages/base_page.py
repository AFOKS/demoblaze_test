from urllib.parse import urljoin

import allure
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:

    timeout = 10

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.timeout)


class WebPage(BasePage):

    path = ""

    def __init__(self, driver, base_url: str):
        super().__init__(driver)
        self.base_url = base_url

    @allure.step("Открыть страницу")
    def open(self):
        self.driver.get(urljoin(self.base_url, self.path))
        return self
