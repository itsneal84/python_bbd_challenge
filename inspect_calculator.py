"""
Calculator Control Inspector
Uses PyWinAuto to discover and display all UI control identifiers
Similar to what Microsoft Inspect.exe shows

This script helps you discover:
- AutomationId (for targeting specific controls)
- ControlType (Button, Text, etc.)
- Class names
- Names and properties

Usage:
    python inspect_calculator.py
"""

from pywinauto import Application, Desktop
from pywinauto.findwindows import ElementNotFoundError
import time
import sys


def launch_calculator():
    """Launch Windows Calculator"""
    try:
        # Try to connect to existing calculator
        app = Application(backend="uia").connect(title_re=".*Calculator.*", timeout=2)
        print("✓ Connected to existing Calculator instance\n")
    except (ElementNotFoundError, Exception):
        # Launch new calculator
        print("Launching Calculator...")
        app = Application(backend="uia").start("calc.exe")
        time.sleep(2)
        print("✓ Calculator launched\n")
    
    return app


def inspect_calculator_controls(app):
    """Inspect and display all calculator controls"""
    
    # Get calculator window
    calc_window = app.window(title_re=".*Calculator.*")
    
    print("=" * 80)
    print("WINDOWS CALCULATOR - CONTROL IDENTIFIERS")
    print("=" * 80)
    print("\nThis information is similar to what Microsoft Inspect.exe shows")
    print("You can use these identifiers in PyWinAuto to interact with controls\n")
    
    # Print full control tree
    print("-" * 80)
    print("FULL CONTROL TREE:")
    print("-" * 80)
    calc_window.print_control_identifiers(depth=None, filename=None)
    
    print("\n" + "=" * 80)
    print("CALCULATOR BUTTON IDENTIFIERS (Quick Reference)")
    print("=" * 80)
    
    # Define known button mappings
    button_mappings = {
        # Numbers
        'num0Button': 'Number 0',
        'num1Button': 'Number 1',
        'num2Button': 'Number 2',
        'num3Button': 'Number 3',
        'num4Button': 'Number 4',
        'num5Button': 'Number 5',
        'num6Button': 'Number 6',
        'num7Button': 'Number 7',
        'num8Button': 'Number 8',
        'num9Button': 'Number 9',
        
        # Basic operators
        'plusButton': 'Plus (+)',
        'minusButton': 'Minus (-)',
        'multiplyButton': 'Multiply (*)',
        'divideButton': 'Divide (/)',
        'equalButton': 'Equals (=)',
        
        # Other operations
        'clearButton': 'Clear (C)',
        'clearEntryButton': 'Clear Entry (CE)',
        'backSpaceButton': 'Backspace',
        'negateButton': 'Negate (+/-)',
        'decimalSeparatorButton': 'Decimal (.)',
        
        # Memory
        'memoryAdd': 'Memory Add (M+)',
        'memorySubtract': 'Memory Subtract (M-)',
        'memoryRecall': 'Memory Recall (MR)',
        'memoryClear': 'Memory Clear (MC)',
        
        # Display
        'CalculatorResults': 'Result Display',
        'CalculatorExpression': 'Expression Display',
    }
    
    print("\n| AutomationId | Description |")
    print("|" + "-" * 40 + "|" + "-" * 37 + "|")
    
    for auto_id, description in button_mappings.items():
        print(f"| {auto_id:<38} | {description:<35} |")
    
    print("\n" + "=" * 80)
    print("EXAMPLE USAGE IN PYWINAUTO")
    print("=" * 80)
    
    example_code = '''
# Find and click the number 2 button
button = calc_window.child_window(auto_id="num2Button", control_type="Button")
button.click()

# Find and click the plus button
button = calc_window.child_window(auto_id="plusButton", control_type="Button")
button.click()

# Get the result display
result = calc_window.child_window(auto_id="CalculatorResults", control_type="Text")
print(result.window_text())
'''
    print(example_code)
    
    print("=" * 80)
    print("\nTEST: Finding specific controls...")
    print("-" * 80)
    
    # Try to find and display info about specific controls
    test_controls = [
        ('num2Button', 'Button'),
        ('plusButton', 'Button'),
        ('equalButton', 'Button'),
        ('CalculatorResults', 'Text'),
    ]
    
    for auto_id, control_type in test_controls:
        try:
            control = calc_window.child_window(auto_id=auto_id, control_type=control_type)
            print(f"✓ Found: {auto_id} ({control_type})")
            print(f"  - Name: {control.window_text()}")
            print(f"  - Rectangle: {control.rectangle()}")
            print(f"  - Is Enabled: {control.is_enabled()}")
            print(f"  - Is Visible: {control.is_visible()}")
            print()
        except Exception as e:
            print(f"✗ Could not find: {auto_id} ({control_type})")
            print(f"  Error: {e}")
            print()


def interactive_mode(app):
    """Interactive mode to click specific buttons"""
    calc_window = app.window(title_re=".*Calculator.*")
    
    print("\n" + "=" * 80)
    print("INTERACTIVE MODE")
    print("=" * 80)
    print("\nTest button clicks interactively!")
    print("Commands:")
    print("  - Enter a number (0-9) to click that button")
    print("  - Enter an operator (+, -, *, /, =) to click that button")
    print("  - Enter 'c' to clear")
    print("  - Enter 'r' to read result")
    print("  - Enter 'q' to quit")
    print()
    
    button_map = {
        '0': 'num0Button', '1': 'num1Button', '2': 'num2Button',
        '3': 'num3Button', '4': 'num4Button', '5': 'num5Button',
        '6': 'num6Button', '7': 'num7Button', '8': 'num8Button',
        '9': 'num9Button', '+': 'plusButton', '-': 'minusButton',
        '*': 'multiplyButton', '/': 'divideButton', '=': 'equalButton',
        'c': 'clearButton',
    }
    
    while True:
        user_input = input("Enter command: ").strip().lower()
        
        if user_input == 'q':
            print("Exiting interactive mode...")
            break
        
        elif user_input == 'r':
            try:
                result = calc_window.child_window(
                    auto_id="CalculatorResults",
                    control_type="Text"
                )
                print(f"Result: {result.window_text()}")
            except Exception as e:
                print(f"Error reading result: {e}")
        
        elif user_input in button_map:
            try:
                button = calc_window.child_window(
                    auto_id=button_map[user_input],
                    control_type="Button"
                )
                button.click()
                print(f"✓ Clicked: {user_input}")
                time.sleep(0.2)
            except Exception as e:
                print(f"Error clicking button: {e}")
        
        else:
            print("Invalid command. Use numbers, operators, 'c', 'r', or 'q'")


def main():
    """Main function"""
    print("\n" + "=" * 80)
    print("CALCULATOR CONTROL INSPECTOR")
    print("=" * 80)
    print("\nThis tool helps you discover Windows Calculator UI controls")
    print("Similar to Microsoft Inspect.exe but in Python!\n")
    
    try:
        # Launch calculator
        app = launch_calculator()
        
        # Inspect controls
        inspect_calculator_controls(app)
        
        # Ask if user wants interactive mode
        print("\n" + "=" * 80)
        response = input("\nWould you like to try interactive mode? (y/n): ").strip().lower()
        
        if response == 'y':
            interactive_mode(app)
        
        print("\n✓ Inspection complete!")
        print("\nNote: Calculator window will remain open for further inspection.")
        print("      You can use Microsoft Inspect.exe for more detailed analysis.")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()