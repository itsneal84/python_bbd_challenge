Feature: Windows Calculator Basic Operations
  As a user
  I want to perform basic arithmetic operations
  So that I can calculate mathematical expressions

  Scenario: Addition of two numbers
    Given the Windows Calculator is open
    When I enter "2" on the calculator
    And I click the "+" button
    And I enter "3" on the calculator
    And I click the "=" button
    Then the result should be "5"

  Scenario: Subtraction of two numbers
    Given the Windows Calculator is open
    When I enter "10" on the calculator
    And I click the "-" button
    And I enter "4" on the calculator
    And I click the "=" button
    Then the result should be "6"

  Scenario: Multiplication of two numbers
    Given the Windows Calculator is open
    When I enter "7" on the calculator
    And I click the "*" button
    And I enter "8" on the calculator
    And I click the "=" button
    Then the result should be "56"

  Scenario: Division of two numbers
    Given the Windows Calculator is open
    When I enter "20" on the calculator
    And I click the "/" button
    And I enter "4" on the calculator
    And I click the "=" button
    Then the result should be "5"

  Scenario: Complex calculation
    Given the Windows Calculator is open
    When I enter "15" on the calculator
    And I click the "+" button
    And I enter "25" on the calculator
    And I click the "-" button
    And I enter "10" on the calculator
    And I click the "=" button
    Then the result should be "30"

  Scenario: Square root of perfect square
    Given the Windows Calculator is open
    # And the calculator is in Scientific mode
    When I enter "16" on the calculator
    And I click the "sqrt" button
    Then the result should be "4"

  Scenario: Square root of 100
    Given the Windows Calculator is open
    # And the calculator is in Scientific mode
    When I enter "100" on the calculator
    And I click the "sqrt" button
    Then the result should be "10"

  Scenario: Square root in calculation
    Given the Windows Calculator is open
    # And the calculator is in Scientific mode
    When I enter "9" on the calculator
    And I click the "sqrt" button
    And I click the "+" button
    And I enter "1" on the calculator
    And I click the "=" button
    Then the result should be "4"
