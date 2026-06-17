@mobile @example
Feature: Mobile Android login
  Example for locators from Artifactory artifact with accessibility id override in conftest.

  Scenario: Login using overridden accessibility ids
    When mobile user logs in with username "standard_user" and password "secret_sauce"
    Then mobile inventory should be visible

  Scenario: Logout via mobile menu labels
    When mobile user logs in with username "standard_user" and password "secret_sauce"
    And mobile user taps "Open Menu"
    And mobile user taps "Logout"
    Then mobile login screen should be visible
