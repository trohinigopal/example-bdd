"""
Login screen locators from the Artifactory artifact.

Format: element_key -> (strategy, value)
Strategies available in artifact: resource_id, xpath, uiautomator
NOT available in artifact: accessibility_id
"""

LOCATORS = {
    "username": ("resource_id", "com.saucedemo.mobile:id/username"),
    "password": ("resource_id", "com.saucedemo.mobile:id/password"),
    "login_button": ("xpath", '//android.widget.Button[@text="LOGIN"]'),
    "inventory_list": ("uiautomator", 'new UiSelector().resourceId("com.saucedemo.mobile:id/inventory_list")'),
    "menu_button": ("resource_id", "com.saucedemo.mobile:id/menu"),
    "logout_button": ("xpath", '//android.widget.TextView[@text="Logout"]'),
}
