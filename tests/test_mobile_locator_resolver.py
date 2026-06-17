"""Unit tests for Android locator override logic (no device required)."""

from artifacts.mobile_locators_android.login_screen import LOCATORS as ARTIFACT_LOCATORS
from conftest import ACCESSIBILITY_ID_OVERRIDES, resolve_android_locator


def test_override_uses_accessibility_id_for_username():
    strategy, value = resolve_android_locator("username")
    assert strategy == "accessibility_id"
    assert value == ACCESSIBILITY_ID_OVERRIDES["username"]


def test_override_uses_accessibility_id_for_login_button():
    strategy, value = resolve_android_locator("login_button")
    assert strategy == "accessibility_id"
    assert value == "Login"


def test_non_overridden_element_falls_back_to_artifact():
    # Remove a key temporarily to test artifact fallback for an element
    # not in ACCESSIBILITY_ID_OVERRIDES — use password which IS overridden,
    # so test artifact-only by checking raw artifact for uiautomator strategy
    from utils.android_locator_resolver import build_locator

    strategy, value = build_locator(
        "inventory_list",
        ARTIFACT_LOCATORS,
        {},  # no overrides
    )
    assert strategy == "uiautomator"
    assert "inventory_list" in value


def test_unknown_element_raises_key_error():
    try:
        resolve_android_locator("unknown_element")
        assert False, "Expected KeyError"
    except KeyError as exc:
        assert "unknown_element" in str(exc)
