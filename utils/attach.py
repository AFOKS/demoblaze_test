import os
import allure
import requests
from selenium.common.exceptions import WebDriverException


def add_screenshot(driver):
    """Прикладывает скриншот текущего состояния браузера в Allure."""
    try:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
    except WebDriverException:
        pass


def add_page_source(driver):
    """Прикладывает HTML-разметку страницы на момент завершения теста."""
    try:
        allure.attach(
            driver.page_source,
            name="page_source",
            attachment_type=allure.attachment_type.HTML,
        )
    except WebDriverException:
        pass


def add_console_logs(driver):
    """Прикладывает логи консоли браузера (поддерживается не всеми браузерами)."""
    try:
        logs = driver.get_log("browser")
        if logs:
            logs_text = "\n".join(
                f"[{entry['level']}] {entry['message']}" for entry in logs
            )
            allure.attach(
                logs_text,
                name="console_logs",
                attachment_type=allure.attachment_type.TEXT,
            )
    except WebDriverException:
        # Firefox и некоторые версии Selenoid не поддерживают get_log("browser")
        pass


def add_video(session_id: str):
    """
    Прикладывает видеозапись сессии из Selenoid.
    Видео становится доступно только ПОСЛЕ завершения сессии (driver.quit()),
    поэтому вызывать эту функцию нужно после quit(), передав сохранённый session_id.
    """
    login = os.getenv("SELENOID_LOGIN")
    password = os.getenv("SELENOID_PASSWORD")
    selenoid_host = os.getenv("SELENOID_URL", "")

    selenoid_host = (
        selenoid_host.removeprefix("https://")
        .removeprefix("http://")
        .removesuffix("/wd/hub")
        .rstrip("/")
    )

    if not (login and password and selenoid_host and session_id):
        return

    video_url = f"https://{selenoid_host}/video/{session_id}.mp4"

    try:
        response = requests.get(video_url, auth=(login, password), timeout=30)
        if response.status_code == 200 and response.content:
            allure.attach(
                response.content,
                name="video",
                attachment_type=allure.attachment_type.MP4,
            )
    except requests.RequestException:
        pass