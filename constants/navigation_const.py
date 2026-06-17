from selenium.webdriver.common.by import By

# --- page locators ---

USERNAME = (By.ID, "user-name")
PASSWORD = (By.ID, "password")
LOGIN_BTN = (By.ID, "login-button")

INVENTORY_LIST = (By.CSS_SELECTOR, ".inventory_list")
MENU_BTN = (By.ID, "react-burger-menu-btn")
ALL_ITEMS = (By.ID, "inventory_sidebar_link")
LOGOUT = (By.ID, "logout_sidebar_link")

# --- label from feature file -> locator ---
# add a new row here when you add a new "user clicks on ..." step

LABEL_MAP = {
    "login": LOGIN_BTN,
    "menu": MENU_BTN,
    "open menu": MENU_BTN,
    "all items": ALL_ITEMS,
    "logout": LOGOUT,
}


def get_label_locator(label):
    key = " ".join(label.strip().lower().split())
    if key not in LABEL_MAP:
        raise KeyError(
            f"'{label}' is not in LABEL_MAP. "
            f"Update constants/navigation_const.py. Known: {list(LABEL_MAP)}"
        )
    return LABEL_MAP[key]
