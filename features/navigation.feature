@navigation
Feature: Label-based navigation
  As a user
  I want to click elements by their on-screen label
  So that scenarios stay readable without scenario outlines

  Background:
    Given the application is open
    When I login with username "standard_user" and password "secret_sauce"

  Scenario: Logout via menu labels
    When user clicks on "Open Menu"
    And user clicks on "Logout"
    Then the page title should contain "Swag Labs"

  Scenario: Navigate using different labels in separate steps
    When user clicks on "Open Menu"
    And user clicks on "All Items"
    Then I should see the inventory page
