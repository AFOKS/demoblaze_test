# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pages.header import Header
from pages.home_page import HomePage  # <-- должен существовать такой файл/класс
import os

BASE_URL = "https://www.demoblaze.com/"


@pytest.fixture(scope="session")
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless=new")

    driver = webdriver.Chrome(service=Service(), options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def page_objects(driver):
    return {
        "header": Header(driver),
    }


@pytest.fixture(scope="function")
def home_page(driver):
    page = HomePage(driver, base_url=BASE_URL)
    page.open()  # если у вас есть метод open(), который делает driver.get(base_url)
    return page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            path = os.path.join(screenshot_dir, f"{item.name}.png")
            driver.save_screenshot(path)