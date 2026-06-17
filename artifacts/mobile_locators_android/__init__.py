"""
Simulates an Android locator package published to Artifactory.

Real-world usage:
    pip install mobile-locators-android==1.2.0  --index-url https://artifactory.company.com/...

This artifact ships resource-id / xpath locators only.
It does NOT include accessibility id — those are applied in conftest.py.
"""

PACKAGE = "com.saucedemo.mobile"
VERSION = "1.0.0"
