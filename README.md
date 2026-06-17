# BDD Selenium Framework

A lightweight **Behavior-Driven Development (BDD)** test framework built with **Python**, **pytest**, **pytest-bdd**, and **Selenium WebDriver**. It uses the **Page Object Model (POM)** pattern with a **label-based navigation** approach — feature files pass on-screen labels (e.g. `"Logout"`, `"Open Menu"`) and the framework resolves them to locators via a central registry.

The demo application under test is [SauceDemo](https://www.saucedemo.com/).

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| [pytest](https://docs.pytest.org/) | Test runner |
| [pytest-bdd](https://pytest-bdd.readthedocs.io/) | Gherkin `.feature` files → Python tests |
| [Selenium](https://www.selenium.dev/) | Browser automation |
| [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) | Auto-downloads ChromeDriver |

---

## Project Structure

```
bdd_framework/
├── config/
│   └── settings.py              # Runtime config (URL, browser, waits)
├── constants/
│   └── navigation_const.py      # Locators + LABEL_MAP registry
├── features/
│   └── navigation.feature       # Gherkin scenarios
├── pages/
│   └── base_page.py             # Shared Selenium actions (POM base)
├── step_defs/
│   └── steps.py                 # BDD step definitions
├── tests/
│   └── test_navigation.py       # Links feature file to pytest
├── utils/
│   └── webdriver_factory.py     # Chrome WebDriver setup
├── reports/
│   └── screenshots/             # Auto-captured on test failure
├── conftest.py                  # pytest fixtures & hooks
├── pytest.ini                   # pytest configuration
├── requirements.txt             # Python dependencies
└── README.md
```

---

## Architecture

### Layer responsibilities

```
┌─────────────────────────────────────────────────────────┐
│  features/navigation.feature   (Gherkin — business language) │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  step_defs/steps.py            (Step definitions — glue code) │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  pages/base_page.py            (Page Object — browser actions) │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  constants/navigation_const.py (Locators + label registry) │
└─────────────────────────────────────────────────────────┘
```

### Execution flow (label click example)

```
Feature:  When user clicks on "Logout"
    │
    ▼
Step def: click_by_label(page, "Logout")
    │
    ▼
BasePage: click_by_label("Logout")
    │
    ▼
get_label_locator("Logout")  →  LABEL_MAP["logout"]  →  LOGOUT locator
    │
    ▼
Selenium: wait + click element
```

---

## Label-Based Navigation

This framework supports readable navigation steps **without Scenario Outline**. Each step passes a different label at runtime:

```gherkin
When user clicks on "Open Menu"
And user clicks on "Logout"
And user clicks on "All Items"
```

### How it works

1. The feature file passes the label in quotes.
2. The step definition captures it via `parsers.parse('user clicks on "{label}"')`.
3. `get_label_locator()` normalizes the label (lowercase, trimmed) and looks it up in `LABEL_MAP`.
4. If the label is not registered, a `KeyError` is raised with a list of known labels.
5. `BasePage.click_by_label()` clicks the resolved element.

### Registry (`LABEL_MAP`)

Defined in `constants/navigation_const.py`:

| Feature label | Maps to |
|---------------|---------|
| `"Login"` | `LOGIN_BTN` |
| `"Open Menu"` / `"Menu"` | `MENU_BTN` |
| `"All Items"` | `ALL_ITEMS` |
| `"Logout"` | `LOGOUT` |

> **Important:** Every label used in a `user clicks on "..."` step must exist in `LABEL_MAP`. There is no dynamic XPath fallback — all navigation labels are explicit.

---

## Constants vs Config vs Input

| Type | Location | Example | When to use |
|------|----------|---------|-------------|
| **Constants** | `constants/navigation_const.py` | Locators, `LABEL_MAP` | Fixed values tied to the UI |
| **Config** | `config/settings.py` + env vars | `BASE_URL`, `HEADLESS` | Values that change per environment |
| **BDD input** | `features/*.feature` | `"standard_user"`, `"Logout"` | Scenario data written by QA/BA |

Python does not use a `.constant` file extension. Constants are regular `.py` modules.

---

## Prerequisites

- Python 3.10+
- Google Chrome installed
- pip

---

## Setup

### 1. Clone / open the project

```bash
cd bdd_framework
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running Tests

### Run all tests

```bash
pytest
```

### Run navigation feature only

```bash
pytest tests/test_navigation.py
```

### Run with marker

```bash
pytest -m navigation
```

### Run headless

```bash
# Windows PowerShell
$env:HEADLESS="true"
pytest

# Windows CMD
set HEADLESS=true && pytest

# macOS / Linux
HEADLESS=true pytest
```

### Run against a different URL

```bash
# Windows PowerShell
$env:BASE_URL="https://www.saucedemo.com/"
pytest
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | `https://www.saucedemo.com/` | Application URL |
| `BROWSER` | `chrome` | Browser name (only Chrome is configured) |
| `HEADLESS` | `false` | Run Chrome without a visible window |
| `WAIT` | `10` | Implicit wait in seconds |

---

## Feature File

`features/navigation.feature` contains two scenarios:

1. **Logout via menu labels** — opens menu, clicks Logout, verifies title.
2. **Navigate using different labels** — opens menu, clicks All Items, verifies inventory page.

```gherkin
Background:
  Given the application is open
  When I login with username "standard_user" and password "secret_sauce"

Scenario: Logout via menu labels
  When user clicks on "Open Menu"
  And user clicks on "Logout"
  Then the page title should contain "Swag Labs"
```

---

## Step Definitions

All steps live in `step_defs/steps.py`:

| Step | Type | Description |
|------|------|-------------|
| `Given the application is open` | Given | Opens `BASE_URL` |
| `When I login with username "..." and password "..."` | When | Fills login form and submits |
| `When user clicks on "..."` | When | Clicks element by label from `LABEL_MAP` |
| `Then the page title should contain "..."` | Then | Asserts browser title |
| `Then I should see the inventory page` | Then | Asserts inventory list is visible |

Steps are registered via `pytest_plugins` in `conftest.py`.

---

## Page Object (`BasePage`)

`pages/base_page.py` provides reusable browser actions:

| Method | Description |
|--------|-------------|
| `open(url)` | Navigate to URL |
| `click(locator)` | Wait for clickable element and click |
| `type_into(locator, text)` | Clear field and type text |
| `is_visible(locator)` | Check if element is visible |
| `click_by_label(label)` | Resolve label → locator → click |

---

## Fixtures (`conftest.py`)

| Fixture | Scope | Description |
|---------|-------|-------------|
| `driver` | function | Creates and quits Chrome per test |
| `base_url` | session | Returns `BASE_URL` from settings |
| `page` | function | Returns `BasePage(driver)` instance |

### Screenshot on failure

If a test fails, a screenshot is saved automatically to:

```
reports/screenshots/<test_name>_<timestamp>.png
```

---

## How to Add a New Clickable Label

### 1. Add the locator in `constants/navigation_const.py`

```python
ABOUT_LINK = (By.ID, "about_sidebar_link")
```

### 2. Register it in `LABEL_MAP`

```python
LABEL_MAP = {
    ...
    "about": ABOUT_LINK,
}
```

### 3. Use it in a feature file

```gherkin
When user clicks on "About"
```

No changes needed in step definitions — the existing `user clicks on "{label}"` step handles it.

---

## How to Add a New Feature

### 1. Create a feature file

```
features/my_feature.feature
```

### 2. Add new steps to `step_defs/steps.py` (if needed)

```python
@then("I should see the about page")
def check_about(page):
    assert page.is_visible(ABOUT_LINK)
```

### 3. Create a test file to bind the feature

```python
# tests/test_my_feature.py
from pytest_bdd import scenarios

scenarios("../features/my_feature.feature")
```

### 4. Run

```bash
pytest tests/test_my_feature.py
```

---

## How to Add a New Page Locator (non-label)

For form fields or elements not used via `user clicks on "..."`:

1. Add the locator constant in `constants/navigation_const.py`.
2. Use it directly in step definitions or page methods.

```python
# step_defs/steps.py
page.type_into(NEW_FIELD, "some value")
```

---

## pytest Configuration

`pytest.ini` settings:

| Setting | Value |
|---------|-------|
| `testpaths` | `tests` |
| `bdd_features_base_dir` | `features` |
| `addopts` | `-v --tb=short` |
| Markers | `navigation` |

---

## Dependencies

```
pytest>=8.0.0
pytest-bdd>=7.0.0
selenium>=4.15.0
webdriver-manager>=4.0.0
```

---

## Troubleshooting

### `KeyError: '...' is not in LABEL_MAP`

The label in your feature file is not registered. Add it to `LABEL_MAP` in `constants/navigation_const.py`.

### `Only chrome is set up right now`

The framework currently supports Chrome only. Install Chrome or set `BROWSER=chrome`.

### ChromeDriver issues

`webdriver-manager` downloads the driver automatically. Ensure you have network access on first run.

### Element not found / timeout

- Increase wait: `WAIT=15 pytest`
- Verify the locator in `navigation_const.py` matches the live DOM
- Run without headless to visually debug: `HEADLESS=false pytest`

### Step definition not found

Ensure `step_defs/steps.py` is listed in `pytest_plugins` inside `conftest.py`.

---

## Design Decisions

- **Registry-only label lookup** — no dynamic XPath; every label must be explicitly mapped for predictable, debuggable tests.
- **Single step file** — all steps in `step_defs/steps.py` for simplicity on a small project.
- **Flat constants** — locators as module-level variables instead of nested classes.
- **Chrome only** — keeps driver setup simple; extend `webdriver_factory.py` for other browsers when needed.

---

## License

Internal / educational use. Update as needed for your organization.
