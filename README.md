# Windows Calculator BDD Test Automation

A complete Behavior-Driven Development (BDD) framework for automating Windows Calculator using Gherkin, Behave, and PyWinAuto.

## 🎯 Overview

This project demonstrates:
1. **Gherkin** - Writing test scenarios in plain English (Given-When-Then)
2. **Behave** - Python BDD framework that maps Gherkin steps to code
3. **PyWinAuto** - Windows UI automation library for interacting with Calculator

## 📁 Project Structure

```
calculator_bdd_test/
│
├── features/
│   ├── calculator.feature          # Gherkin test scenarios
│   ├── environment.py               # Behave hooks (setup/teardown)
│   └── steps/
│       └── calculator_steps.py      # Step definitions (Gherkin → Python)
│
├── utils/
│   └── calculator_wrapper.py       # PyWinAuto wrapper for Calculator
│
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 🚀 Installation

### Prerequisites
- **Windows OS** (Windows 10 or 11)
- **Python 3.7+**
- **Windows Calculator** (pre-installed on Windows)

### Setup Steps

1. **Clone or download this project**

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

This installs:
- `behave` - BDD test framework
- `pywinauto` - Windows UI automation
- `comtypes` - COM automation support
- `pywin32` - Windows API bindings

## 🎮 Usage

### Running All Tests

From the project root directory:

```bash
behave
```

### Running Specific Scenarios

Run tests with a specific tag:
```bash
behave --tags=@addition
```

Run a specific feature file:
```bash
behave features/calculator.feature
```

### Verbose Output

```bash
behave -v
```

### Dry Run (check syntax without execution)

```bash
behave --dry-run
```

## 📝 Writing Test Scenarios

### Gherkin Syntax

Tests are written in `features/calculator.feature` using Gherkin:

```gherkin
Feature: Windows Calculator Basic Operations
  
  Scenario: Addition of two numbers
    Given the Windows Calculator is open
    When I enter "2" on the calculator
    And I click the "+" button
    And I enter "3" on the calculator
    And I click the "=" button
    Then the result should be "5"
```

### Available Steps

**Given Steps:**
- `Given the Windows Calculator is open`

**When Steps:**
- `When I enter "{number}" on the calculator`
- `When I click the "{operator}" button`
  - Operators: `+`, `-`, `*`, `/`, `=`

**Then Steps:**
- `Then the result should be "{expected_result}"`

## 🔧 Technical Implementation

### 1. Gherkin → Behave Mapping

Behave uses decorators to map Gherkin steps to Python functions:

```python
@given('the Windows Calculator is open')
def step_open_calculator(context):
    context.calculator = CalculatorApp()
    context.calculator.launch()
```

### 2. PyWinAuto Integration

The `CalculatorApp` wrapper uses PyWinAuto to:
- Launch Calculator: `Application(backend="uia").start("calc.exe")`
- Find UI controls using AutomationId
- Simulate clicks: `button.click()`
- Read display values: `result_display.window_text()`

### 3. Control Identifiers

Windows Calculator button AutomationIds:

| Button | AutomationId |
|--------|-------------|
| 0-9    | num0Button - num9Button |
| +      | plusButton |
| -      | minusButton |
| *      | multiplyButton |
| /      | divideButton |
| =      | equalButton |
| C      | clearButton |
| Display | CalculatorResults |

## 🔍 Inspecting UI Controls

### Using Microsoft Inspect

1. **Download Inspect** (part of Windows SDK)
   - Or use the built-in Inspect.exe from `C:\Program Files (x86)\Windows Kits\10\bin\<version>\x64\`

2. **Launch Inspect.exe**

3. **Open Calculator**

4. **Hover over Calculator buttons** to see:
   - AutomationId
   - ControlType
   - Name
   - Other properties

### Using Python to Print Controls

```python
from utils.calculator_wrapper import CalculatorApp

calc = CalculatorApp()
calc.launch()
calc.print_control_identifiers()  # Prints all control IDs
```

## 🧪 Example Test Run

```
============================================================
Starting Calculator BDD Test Suite
============================================================

============================================================
Feature: Windows Calculator Basic Operations
============================================================

Scenario: Addition of two numbers
------------------------------------------------------------
✓ Calculator opened and cleared
✓ Entered number: 2
✓ Clicked operator: +
✓ Entered number: 3
✓ Clicked operator: =
✓ Result verified: 5 == 5
✓ Calculator closed
✓ Scenario PASSED
------------------------------------------------------------

1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 0 skipped
6 steps passed, 0 failed, 0 skipped, 0 undefined
```

## 📚 Key Concepts

### BDD (Behavior-Driven Development)
- Write tests in **business language** (Gherkin)
- Tests describe **behavior**, not implementation
- **Living documentation** that stakeholders can read

### Gherkin Keywords
- **Feature**: High-level description
- **Scenario**: Specific test case
- **Given**: Initial context/setup
- **When**: Action being tested
- **Then**: Expected outcome
- **And**: Additional steps of same type

### PyWinAuto Backends
- **UIA (UI Automation)**: Modern Windows apps, Calculator
- **Win32**: Legacy Windows applications

## 🐛 Troubleshooting

### Calculator doesn't launch
```python
# Ensure Calculator path is correct
# On Windows 10/11, use: "calc.exe"
```

### Control not found
```python
# Use calc.print_control_identifiers() to inspect
# Or use Microsoft Inspect tool
```

### Timing issues
```python
# Add sleep delays in calculator_wrapper.py
time.sleep(0.5)  # Wait after clicks
```

### Permission errors
- Run command prompt as **Administrator**
- Check Windows UAC settings

## 🎓 Learning Resources

- **Behave Documentation**: https://behave.readthedocs.io/
- **PyWinAuto Docs**: https://pywinauto.readthedocs.io/
- **Gherkin Reference**: https://cucumber.io/docs/gherkin/
- **UI Automation**: https://docs.microsoft.com/en-us/windows/win32/winauto/

## 🔄 Extending the Framework

### Add New Operations

1. **Add Gherkin scenario** in `calculator.feature`
2. **Add step definitions** in `calculator_steps.py` if needed
3. **Add methods** to `calculator_wrapper.py` for new controls

### Example: Adding Square Root

**Feature file:**
```gherkin
Scenario: Square root calculation
  Given the Windows Calculator is open
  When I enter "16" on the calculator
  And I click the "sqrt" button
  Then the result should be "4"
```

**Wrapper method:**
```python
def click_square_root(self):
    button = self.calculator_window.child_window(
        auto_id="squareRootButton",
        control_type="Button"
    )
    button.click()
```

**Step definition:**
```python
@when('I click the "sqrt" button')
def step_click_sqrt(context):
    context.calculator.click_square_root()
```

## 📊 Advanced Features

### Parallel Execution
```bash
behave --processes 4
```

### HTML Reports
```bash
behave -f html -o reports/report.html
```

### JSON Output
```bash
behave -f json -o reports/results.json
```

## ✅ Best Practices

1. **Keep scenarios independent** - Each should run standalone
2. **Use descriptive names** - Make intent clear
3. **One assertion per Then** - Keep focused
4. **Clean state between tests** - Use environment.py hooks
5. **Meaningful test data** - Use realistic examples

## 🤝 Contributing

Feel free to extend this framework with:
- More calculator operations (memory, scientific functions)
- Enhanced error handling
- Screenshot capture on failure
- Performance metrics
- Cross-application testing

## 📄 License

This project is provided as-is for educational purposes.

---

**Happy Testing! 🧪✨**