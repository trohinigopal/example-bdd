import os
from datetime import datetime

import pytest

from artifacts.mobile_locators_android.login_screen import LOCATORS as ARTIFACT_LOCATORS
from config.settings import BASE_URL, SCREENSHOT_DIR
from utils.android_locator_resolver import build_locator
from utils.mobile_driver_factory import create_mobile_driver
from utils.webdriver_factory import create_driver

pytest_plugins = [
    "step_defs.steps",
    "step_defs.mobile_steps",
]

# ---------------------------------------------------------------------------
# Android: accessibility id overrides for locators from Artifactory artifact
# The artifact package (artifacts/mobile_locators_android) ships resource-id /
# xpath only. QA adds accessibility id here in conftest when the app supports it.
# ---------------------------------------------------------------------------

ACCESSIBILITY_ID_OVERRIDES = {
    "username": "Username",
    "password": "Password",
    "login_button": "Login",
    "inventory_list": "Inventory list",
    "menu_button": "Open navigation menu",
    "logout_button": "Logout",
}


def resolve_android_locator(element_key: str) -> tuple[str, str]:
    """
    Pick Android locator for an element key.

    Priority:
      1. accessibility id from ACCESSIBILITY_ID_OVERRIDES (conftest)
      2. locator from Artifactory artifact package
    """
    return build_locator(element_key, ARTIFACT_LOCATORS, ACCESSIBILITY_ID_OVERRIDES)


@pytest.fixture
def get_android_locator():
    """Expose resolver to mobile page objects and step defs."""
    return resolve_android_locator


@pytest.fixture
def driver():
    driver = create_driver()
    yield driver
    driver.quit()


@pytest.fixture
def mobile_driver():
    if not os.getenv("APPIUM_SERVER_URL"):
        pytest.skip("Set APPIUM_SERVER_URL to run mobile tests (e.g. http://127.0.0.1:4723)")

    driver = create_mobile_driver()
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
        driver = item.funcargs.get("driver") or item.funcargs.get("mobile_driver")
        if driver:
            name = item.name.replace("/", "_")
            path = SCREENSHOT_DIR / f"{name}_{datetime.now():%Y%m%d_%H%M%S}.png"
            driver.save_screenshot(str(path))
