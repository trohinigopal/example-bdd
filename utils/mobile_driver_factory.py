import os

import pytest


def create_mobile_driver():
    try:
        from appium import webdriver
        from appium.options.android import UiAutomator2Options
    except ImportError as exc:
        raise ImportError(
            "Install Appium to run mobile tests: pip install Appium-Python-Client"
        ) from exc

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = os.getenv("ANDROID_DEVICE", "emulator-5554")
    options.app_package = os.getenv("ANDROID_APP_PACKAGE", "com.saucedemo.mobile")
    options.app_activity = os.getenv("ANDROID_APP_ACTIVITY", ".MainActivity")
    options.automation_name = "UiAutomator2"

    return webdriver.Remote(
        command_executor=os.environ["APPIUM_SERVER_URL"],
        options=options,
    )
