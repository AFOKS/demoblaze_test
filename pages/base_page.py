from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException


class BasePage:
    def __init__(self, driver, base_url: str = "https://www.demoblaze.com/"):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)

    def open(self, path: str = ""):
        self.driver.get(f"{self.base_url}{path}")
        return self

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            el.click()
        except ElementClickInterceptedException:
            # Карусель/анимация могла перекрыть элемент в момент клика — кликаем через JS
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            self.driver.execute_script("arguments[0].click();", el)
        return self