from config.settings import WAIT
from utils.android_locator_resolver import build_locator


class MobileBasePage:
    """Example mobile POM — locators resolved via conftest override + artifact."""

    def __init__(self, driver, get_locator):
        self.driver = driver
        self.get_locator = get_locator
        self.wait = WAIT

    def _find(self, element_key):
        strategy, value = self.get_locator(element_key)
        return self._find_by_strategy(strategy, value)

    def _find_by_strategy(self, strategy, value):
        # Appium is optional; this example shows the wiring pattern.
        try:
            from appium.webdriver.common.appiumby import AppiumBy
        except ImportError as exc:
            raise ImportError(
                "Install Appium to run mobile tests: pip install Appium-Python-Client"
            ) from exc

        by_map = {
            "accessibility_id": AppiumBy.ACCESSIBILITY_ID,
            "resource_id": AppiumBy.ID,
            "xpath": AppiumBy.XPATH,
            "uiautomator": AppiumBy.ANDROID_UIAUTOMATOR,
        }

        if strategy not in by_map:
            raise ValueError(f"Unsupported locator strategy: {strategy}")

        return self.driver.find_element(by_map[strategy], value)

    def click(self, element_key):
        self._find(element_key).click()

    def type_into(self, element_key, text):
        field = self._find(element_key)
        field.clear()
        field.send_keys(text)

    def is_visible(self, element_key):
        try:
            return self._find(element_key).is_displayed()
        except Exception:
            return False

    def login(self, username, password):
        self.type_into("username", username)
        self.type_into("password", password)
        self.click("login_button")
