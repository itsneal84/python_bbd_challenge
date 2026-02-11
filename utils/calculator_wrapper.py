"""
Calculator Automation Wrapper using PyWinAuto
This module provides a clean interface to interact with Windows Calculator
"""
from pywinauto import Application, Desktop
from pywinauto.findwindows import ElementNotFoundError
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CalculatorApp:
    """Wrapper class for Windows Calculator automation"""

    def __init__(self):
        self.app = None
        self.calculator_window = None
        self.main_window = None

    def launch(self):
        """Launch Windows Calculator application"""
        try:
            # Try to connect to existing calculator first
            self.app = Application(backend="uia").connect(title_re=".*Calculator.*", timeout=2)
            logger.info("Connected to existing Calculator instance")
        except (ElementNotFoundError, Exception):
            # Launch new calculator instance
            logger.info("Launching new Calculator instance")
            self.app = Application(backend="uia").start("calc.exe")

        # Get the calculator window
        self.calculator_window = self.app.window(title_re=".*Calculator.*")
        # self.calculator_window.wait('ready').set_focus()
        logger.info("Calculator window ready")
            
        return self
    
    def close(self):
        """Close the calculator application"""
        if self.calculator_window:
            try:
                self.calculator_window.close()
                logger.info("Calculator closed")
            except Exception as e:
                logger.warning(f"Error closing calculator: {e}")

    def clear(self):
        """Clear the calculator display"""
        try:
            # Press Clear button (C)
            clear_button = self.calculator_window.child_window(auto_id="clearButton", control_type="Button")
            # clear_button.click()
            clear_button.click_input()
            time.sleep(0.3)
            logger.info("Calculator cleared")
        except Exception as e:
            logger.warning(f"Could not find clear button, trying keyboard shortcut: {e}")
            # Alternative: use Escape key
            self.calculator_window.type_keys("{ESC}")
            time.sleep(0.3)

    def switch_to_scientific_mode(self):
        """
        Switch calculator to Scientific mode
        Required for advanced functions like square root, power, trig functions
        """
        try:
            # Open navigation menu
            menu_button = self.calculator_window.child_window(
                auto_id="TogglePaneButton",
                control_type="Button"
            )
            menu_button.click()
            time.sleep(0.3)
            
            # Click Scientific option
            scientific_button = self.calculator_window.child_window(
                title="Scientific Calculator",
                control_type="ListItem"
            )
            scientific_button.click()
            time.sleep(0.5)
            logger.info("Switched to Scientific mode")
        except Exception as e:
            logger.error(f"Error switching to Scientific mode: {e}")
            raise

    def click_number(self, number):
        """
        Click a number button on the calculator
        
        Args:
            number (str): The number to click (0-9)
        """
        try:
            # Map numbers to their AutomationId
            number_ids = {
                '0': 'num0Button',
                '1': 'num1Button',
                '2': 'num2Button',
                '3': 'num3Button',
                '4': 'num4Button',
                '5': 'num5Button',
                '6': 'num6Button',
                '7': 'num7Button',
                '8': 'num8Button',
                '9': 'num9Button',
            }
            
            if number in number_ids:
                button = self.calculator_window.child_window(
                    auto_id=number_ids[number], 
                    control_type="Button"
                )
                button.click()
                time.sleep(0.2)
                logger.info(f"Clicked number: {number}")
            else:
                raise ValueError(f"Invalid number: {number}")
                
        except Exception as e:
            logger.error(f"Error clicking number {number}: {e}")
            raise
    
    def click_operator(self, operator):
        """
        Click an operator button on the calculator
        
        Args:
            operator (str): The operator (+, -, *, /, sqrt)
        """
        try:
            # Map operators to their AutomationId
            operator_ids = {
                '+': 'plusButton',
                '-': 'minusButton',
                '*': 'multiplyButton',
                '/': 'divideButton',
                '=': 'equalButton',
                'sqrt': 'squareRootButton'
            }
            
            if operator in operator_ids:
                button = self.calculator_window.child_window(
                    auto_id=operator_ids[operator],
                    control_type="Button"
                )
                button.click()
                time.sleep(0.2)
                logger.info(f"Clicked operator: {operator}")
            else:
                raise ValueError(f"Invalid operator: {operator}")
                
        except Exception as e:
            logger.error(f"Error clicking operator {operator}: {e}")
            raise

    def enter_number(self, number_string):
        """
        Enter a multi-digit number by clicking individual digits
        
        Args:
            number_string (str): The number to enter (e.g., "123")
        """
        for digit in number_string:
            if digit.isdigit():
                self.click_number(digit)
            else:
                raise ValueError(f"Invalid digit in number: {digit}")
    
    def get_result(self):
        """
        Get the current result displayed on the calculator
        
        Returns:
            str: The displayed result
        """
        try:
            # The result is displayed in a text element with AutomationId "CalculatorResults"
            result_display = self.calculator_window.child_window(
                auto_id="CalculatorResults",
                control_type="Text"
            )
            
            # Get the display text
            result_text = result_display.window_text()
            
            # The result format is "Display is {number}"
            # Extract just the number
            if "Display is" in result_text:
                result = result_text.replace("Display is", "").strip()
            else:
                result = result_text.strip()
            
            logger.info(f"Retrieved result: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error getting result: {e}")
            raise
    
    def print_control_identifiers(self):
        """
        Helper method to print all control identifiers in the calculator window
        Useful for discovering AutomationIds
        """
        print("\n=== Calculator Control Identifiers ===\n")
        try:
            self.calculator_window.print_control_identifiers()
        except Exception as e:
            logger.error(f"Error printing control identifiers: {e}")


# Example usage and testing
if __name__ == "__main__":
    print("Testing Calculator Automation...")
    
    calc = CalculatorApp()
    
    try:
        # Launch calculator
        calc.launch()
        time.sleep(1)
        
        # Optional: Print control identifiers for inspection
        # calc.print_control_identifiers()
        
        # Test: 2 + 3 = 5
        print("\nTest: 2 + 3 = 5")
        calc.clear()
        calc.enter_number("2")
        calc.click_operator("+")
        calc.enter_number("3")
        calc.click_operator("=")
        result = calc.get_result()
        print(f"Result: {result}")
        
        # Test: 10 - 4 = 6
        print("\nTest: 10 - 4 = 6")
        calc.clear()
        calc.enter_number("10")
        calc.click_operator("-")
        calc.enter_number("4")
        calc.click_operator("=")
        result = calc.get_result()
        print(f"Result: {result}")
        
        print("\n✓ All tests completed!")
        
    except Exception as e:
        print(f"\n✗ Error during test: {e}")
        
    finally:
        # Keep calculator open for inspection
        input("\nPress Enter to close calculator...")
        calc.close()