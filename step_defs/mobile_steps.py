import pytest
from pytest_bdd import parsers, then, when

from constants.mobile_const import INVENTORY_LIST, LOGIN_BUTTON, LOGOUT_BUTTON, MENU_BUTTON
from pages.mobile_base_page import MobileBasePage


@pytest.fixture
def mobile_page(mobile_driver, get_android_locator):
    return MobileBasePage(mobile_driver, get_android_locator)


@when(parsers.parse('mobile user logs in with username "{username}" and password "{password}"'))
def mobile_login(mobile_page, username, password):
    mobile_page.login(username, password)


@when(parsers.parse('mobile user taps "{label}"'))
def mobile_tap_label(mobile_page, label):
    label_map = {
        "open menu": MENU_BUTTON,
        "logout": LOGOUT_BUTTON,
    }
    key = " ".join(label.strip().lower().split())
    if key not in label_map:
        raise KeyError(f"Unknown mobile label '{label}'. Add mapping in mobile_steps.py")
    mobile_page.click(label_map[key])


@then("mobile inventory should be visible")
def mobile_inventory_visible(mobile_page):
    assert mobile_page.is_visible(INVENTORY_LIST), "Mobile inventory not visible"


@then("mobile login screen should be visible")
def mobile_login_screen_visible(mobile_page):
    assert mobile_page.is_visible(LOGIN_BUTTON), "Mobile login screen not visible"
