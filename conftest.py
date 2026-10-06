import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pages.header import Header
from pages.home_page import HomePage
from utils.attach import (
    add_screenshot,
    add_page_source,
    add_console_logs,
    add_video,
)

load_dotenv()


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        pytest.fail(f"Не задана переменная окружения {name} (см. .env.example)")
    return value


def pytest_addoption(parser):
    parser.addoption(
        "--site-url",
        default="https://www.demoblaze.com/",
        help="URL тестируемого сайта",
    )
    parser.addoption(
        "--browser",
        default="chrome",
        choices=("chrome", "firefox"),
        help="Браузер для запуска тестов",
    )
    parser.addoption(
        "--browser-version",
        default="148.0",
        help="Версия браузера в Selenoid",
    )
    parser.addoption(
        "--resolution",
        default="1920x1080",
        help="Разрешение экрана браузера в формате WIDTHxHEIGHT",
    )


@pytest.fixture(scope="session")
def site_url(request):
    return request.config.getoption("--site-url")


@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def browser_version(request):
    return request.config.getoption("--browser-version")


@pytest.fixture(scope="session")
def resolution(request):
    return request.config.getoption("--resolution")


@pytest.fixture(scope="session")
def valid_username():
    return require_env("DEMOBLAZE_USERNAME")


@pytest.fixture(scope="session")
def valid_password():
    return require_env("DEMOBLAZE_PASSWORD")


@pytest.fixture(scope="session")
def selenoid_url():
    login = require_env("SELENOID_LOGIN")
    password = require_env("SELENOID_PASSWORD")
    selenoid_host = require_env("SELENOID_URL")

    # Убираем протокол и /wd/hub, если они случайно указаны в .env
    selenoid_host = selenoid_host.removeprefix("https://")
    selenoid_host = selenoid_host.removeprefix("http://")
    selenoid_host = selenoid_host.removesuffix("/wd/hub")
    selenoid_host = selenoid_host.rstrip("/")

    return f"https://{login}:{password}@{selenoid_host}/wd/hub"


@pytest.fixture(scope="function")
def driver(browser, browser_version, resolution, selenoid_url, request):
    if browser == "chrome":
        options = ChromeOptions()
    elif browser == "firefox":
        options = FirefoxOptions()
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    options.set_capability("browserName", browser)
    options.set_capability("browserVersion", browser_version)
    options.set_capability(
        "selenoid:options",
        {
            "name": request.node.name,
            "sessionTimeout": "60m",
            "screenResolution": f"{resolution}x24",
            "timeZone": "UTC",
            "labels": {"project": "demoblaze_test"},
            "enableVNC": True,
            "enableVideo": True,
            "enableHAR": False,
            "enableLog": True,
        },
    )

    remote_driver = webdriver.Remote(
        command_executor=selenoid_url,
        options=options,
    )

    yield remote_driver

    # session_id нужно сохранить ДО quit(): после закрытия сессии он недоступен
    session_id = remote_driver.session_id

    # quit() обязан выполниться, даже если вложения не удалось снять,
    # иначе сессия в Selenoid останется висеть до sessionTimeout
    try:
        add_screenshot(remote_driver)
        add_page_source(remote_driver)
        add_console_logs(remote_driver)
    finally:
        remote_driver.quit()

    # Видео в Selenoid финализируется только после закрытия сессии
    add_video(session_id)


@pytest.fixture(scope="function")
def header(driver):
    return Header(driver)


@pytest.fixture(scope="function")
def home_page(driver, site_url):
    return HomePage(driver, base_url=site_url).open()
