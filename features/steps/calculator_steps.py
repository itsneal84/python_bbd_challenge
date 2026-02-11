"""
Step definitions for Calculator BDD tests
This maps Gherkin steps to Python code using PyWinAuto
"""
from behave import given, when, then
import sys
import os

# Add parent directory to path to import calculator_wrapper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils.calculator_wrapper import CalculatorApp
import time

@given('the Windows Calculator is open')
def step_open_calculator(context):
    """
    Opens Windows Calculator and stores reference in context
    This step is called by: Given the Windows Calculator is open
    """
    context.calculator = CalculatorApp()
    context.calculator.launch()
    context.calculator.clear()  # Start with a clean slate
    print("✓ Calculator opened and cleared")

@given(u'the calculator is in Scientific mode')
def step_switch_to_scientific(context):
    """
    Switches calculator to Scientific mode
    This step is called by: Given the calculator is in Scientific mode
    
    Required for advanced functions like square root, power, trigonometry
    """
    context.calculator.switch_to_scientific_mode()
    print("✓ Calculator switched to Scientific mode")

@when('I enter "{number}" on the calculator')
def step_enter_number(context, number):
    """
    Enters a number on the calculator by clicking digit buttons
    This step is called by: When I enter "2" on the calculator
    
    Args:
        number (str): The number to enter (can be multi-digit)
    """
    context.calculator.enter_number(number)
    print(f"✓ Entered number: {number}")

@when('I click the "{operator}" button')
def step_click_operator(context, operator):
    """
    Clicks an operator button on the calculator
    This step is called by: When I click the "+" button
    
    Args:
        operator (str): The operator to click (+, -, *, /, =)
    """
    context.calculator.click_operator(operator)
    print(f"✓ Clicked operator: {operator}")

@then('the result should be "{expected_result}"')
def step_verify_result(context, expected_result):
    """
    Verifies the calculator displays the expected result
    This step is called by: Then the result should be "5"
    
    Args:
        expected_result (str): The expected result to verify
    """
    # Give calculator a moment to compute
    time.sleep(0.5)
    
    # Get the actual result from calculator
    actual_result = context.calculator.get_result()
    
    # Normalize both results for comparison (remove commas, spaces, etc.)
    normalized_actual = actual_result.replace(',', '').replace(' ', '')
    normalized_expected = expected_result.replace(',', '').replace(' ', '')
    
    # Assert the results match
    assert normalized_actual == normalized_expected, \
        f"Expected result '{normalized_expected}' but got '{normalized_actual}'"
    
    print(f"✓ Result verified: {actual_result} == {expected_result}")