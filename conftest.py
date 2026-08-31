import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pages.header import Header
import os

BASE_URL = "https://www.demoblaze.com/"


@pytest.fixture(scope="session")
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Для headless-режима в CI раскомментируйте:
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


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call, report):
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            path = os.path.join(screenshot_dir, f"{item.name}.png")
            driver.save_screenshot(path)
            # Allure подхватит скриншот из папки allure-results при аттаче,
            # но здесь мы просто сохраняем локально