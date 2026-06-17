from artifacts.mobile_locators_android.login_screen import LOCATORS as ARTIFACT_LOCATORS


def build_locator(element_key, artifact_locators, accessibility_overrides):
    """
    Resolve Android locator:
    1. accessibility id override (from conftest) wins
    2. otherwise use locator from Artifactory artifact package
    """
    if element_key in accessibility_overrides:
        return ("accessibility_id", accessibility_overrides[element_key])

    if element_key not in artifact_locators:
        known = sorted(artifact_locators.keys())
        raise KeyError(
            f"Unknown mobile element '{element_key}'. "
            f"Known artifact keys: {known}"
        )

    return artifact_locators[element_key]
