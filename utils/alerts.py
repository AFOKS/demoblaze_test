from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def accept_alert(driver, timeout: int = 5) -> str:

    alert = WebDriverWait(driver, timeout).until(EC.alert_is_present())
    text = alert.text
    alert.accept()
    return text
