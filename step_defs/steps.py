import pytest
from pytest_bdd import given, parsers, then, when

from constants.navigation_const import INVENTORY_LIST, LOGIN_BTN, PASSWORD, USERNAME
from pages.base_page import BasePage


@pytest.fixture
def page(driver):
    return BasePage(driver)


@given("the application is open")
def open_application(driver, base_url):
    driver.get(base_url)


@when(parsers.parse('I login with username "{username}" and password "{password}"'))
def login(page, username, password):
    page.type_into(USERNAME, username)
    page.type_into(PASSWORD, password)
    page.click(LOGIN_BTN)


@when(parsers.parse('user clicks on "{label}"'))
def click_by_label(page, label):
    page.click_by_label(label)


@then(parsers.parse('the page title should contain "{text}"'))
def check_title(driver, text):
    assert text.lower() in driver.title.lower()


@then("I should see the inventory page")
def check_inventory(page):
    assert page.is_visible(INVENTORY_LIST), "Inventory page did not load"
