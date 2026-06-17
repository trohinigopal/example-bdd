from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config.settings import BROWSER, HEADLESS, WAIT


def create_driver():
    if BROWSER.lower() != "chrome":
        raise ValueError(f"Only chrome is set up right now. Got: {BROWSER}")

    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    driver.implicitly_wait(WAIT)
    driver.maximize_window()
    return driver
