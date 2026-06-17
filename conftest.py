from datetime import datetime

import pytest

from config.settings import BASE_URL, SCREENSHOT_DIR
from utils.webdriver_factory import create_driver

pytest_plugins = ["step_defs.steps"]


@pytest.fixture
def driver():
    driver = create_driver()
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            name = item.name.replace("/", "_")
            path = SCREENSHOT_DIR / f"{name}_{datetime.now():%Y%m%d_%H%M%S}.png"
            driver.save_screenshot(str(path))
