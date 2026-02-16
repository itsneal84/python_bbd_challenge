# TeamCity Setup Guide for Windows Calculator BDD Tests

This guide explains how to set up and run the Windows Calculator BDD tests in TeamCity.

## 📋 Prerequisites

### TeamCity Requirements
- **TeamCity Server** (any recent version)
- **TeamCity Build Agent** running on **Windows 10/11**
- Agent must have **UI interaction capabilities** (not running as a service in session 0)

### Agent Configuration
**CRITICAL**: The TeamCity agent must be able to interact with the Windows UI:

1. **Run agent as a regular user process** (not as a Windows service)
2. **User must be logged in** during test execution
3. **Desktop should be unlocked** (tests need to interact with Calculator GUI)

### Software on Build Agent
- **Python 3.7+** installed and in PATH
- **pip** installed
- **Windows Calculator** (pre-installed on Windows)
- **Git** (for source control checkout)

## 🏗️ TeamCity Project Structure

### Recommended Setup

```
Project: Windows Calculator Tests
  └── Build Configuration: Calculator BDD Tests
      ├── VCS Root: Your Git Repository
      ├── Build Steps (see below)
      └── Artifacts & Reports
```

## 🔧 Build Configuration Steps

### Step 1: VCS Checkout
TeamCity will automatically checkout your repository.

### Step 2: Python Virtual Environment Setup
- **Runner Type**: Command Line
- **Step Name**: Setup Python Environment
- **Run**: Custom script

```batch
REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies
pip install -r requirements.txt

REM Verify installations
pip list
```

### Step 3: Run BDD Tests
- **Runner Type**: Command Line
- **Step Name**: Run Behave Tests
- **Run**: Custom script

```batch
REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run behave with TeamCity-compatible output
behave --junit --junit-directory test-results --format json --outfile test-results/behave-results.json --format pretty

REM Exit with proper code
exit /b %ERRORLEVEL%
```

### Alternative: Run with HTML Report
```batch
call venv\Scripts\activate.bat

REM Create reports directory
if not exist "reports" mkdir reports

REM Run behave with multiple formatters
behave --junit --junit-directory test-results --format html --outfile reports/behave-report.html --format pretty
```

## 📊 Build Features

### 1. XML Test Reporting
**Build Feature**: XML report processing
- **Report Type**: Ant JUnit
- **Monitoring Rules**: `test-results/**/*.xml`

This will show test results in TeamCity's Tests tab.

### 2. Build Artifacts
Configure artifacts to preserve test reports:

**Artifact Paths**:
```
test-results/** => test-results.zip
reports/** => reports.zip
```

### 3. Build Failure Conditions
Add failure condition:
- **Fail build if**: at least one test failed
- **Fail build if**: build step fails

## 🎯 Complete Build Configuration (UI)

### General Settings
- **Name**: Calculator BDD Tests
- **Build number format**: %build.counter%
- **Artifact paths**: 
  ```
  test-results/**/* => test-results.zip
  reports/**/* => reports.zip
  ```

### VCS Settings
- Attach your VCS root
- **VCS checkout mode**: Automatically on agent

### Build Steps

#### Step 1: Install Dependencies
```
Step name: Install Dependencies
Runner type: Command Line
Run: Custom script

Script:
python -m venv venv
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 2: Run Tests
```
Step name: Run BDD Tests
Runner type: Command Line
Run: Custom script

Script:
call venv\Scripts\activate.bat
if not exist "test-results" mkdir test-results
behave --junit --junit-directory test-results --format pretty
```

### Build Features
1. **XML report processing**
   - Report type: Ant JUnit
   - Monitoring rules: `test-results/**/*.xml`

2. **Build files cleaner** (optional)
   - Checkout directory: Selected files
   - Patterns: `venv/`, `*.pyc`, `__pycache__/`

## 🐍 Alternative: Python Build Runner

If you have the Python Build Runner plugin installed:

### Step 1: Install Dependencies
- **Runner Type**: Python
- **Command**: custom script
- **Script**: 
  ```python
  import subprocess
  subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)
  ```

### Step 2: Run Tests
- **Runner Type**: Python
- **Command**: custom script
- **Script**:
  ```python
  import subprocess
  import sys
  result = subprocess.run(['behave', '--junit', '--junit-directory', 'test-results', '--format', 'pretty'])
  sys.exit(result.returncode)
  ```

## 🔒 Agent Requirements

Set up an agent requirement to ensure tests only run on agents with UI capability:

**Parameter**: `system.agent.name`
**Condition**: contains
**Value**: `windows-ui-agent` (or your specific agent name)

## ⚙️ Build Parameters

Define these parameters for flexibility:

| Name | Value | Description |
|------|-------|-------------|
| `env.PYTHONUNBUFFERED` | `1` | Ensure Python output appears in real-time |
| `python.version` | `3.11` | Python version (informational) |
| `behave.tags` | (empty) | Optional: Filter tests by tags |

## 📝 Advanced Configuration

### Running Specific Test Tags

To run only specific scenarios with tags:

```batch
call venv\Scripts\activate.bat
behave --junit --junit-directory test-results --tags=@addition --format pretty
```

### Parallel Execution (Experimental)

```batch
call venv\Scripts\activate.bat
behave --junit --junit-directory test-results --processes 2 --parallel-element scenario
```

**Note**: Parallel execution may cause issues with Calculator UI automation.

### Screenshot on Failure

Add to `environment.py` after_scenario hook:

```python
def after_scenario(context, scenario):
    if scenario.status == "failed":
        from PIL import ImageGrab
        import os
        screenshot = ImageGrab.grab()
        screenshot.save(f"test-results/{scenario.name}_failure.png")
```

Then update artifact paths to include screenshots:
```
test-results/**/*.png => screenshots.zip
```

## 🔍 Troubleshooting

### Issue: Tests fail with "Calculator not found"

**Solution**: Ensure the TeamCity agent:
1. Is running as a regular user process (not a service)
2. Has an active desktop session
3. User is logged in and desktop is unlocked

### Issue: Agent runs as Windows Service

**Solution**: Reconfigure agent to run as a console application:

1. Stop the TeamCity Build Agent service
2. Open `conf/buildAgent.properties`
3. Run `bin/agent.bat start` manually when user is logged in
4. Or set up agent to auto-start on user login (not as a service)

### Issue: Python not found

**Solution**: 
1. Install Python on the build agent
2. Add Python to system PATH
3. Restart the agent
4. Verify with: `python --version`

### Issue: Display is not available

**Solution**: 
```batch
REM Set display environment variable if needed
set DISPLAY=:0
```

### Issue: Timing/synchronization issues

**Solution**: Increase wait times in `calculator_wrapper.py`:
```python
time.sleep(0.5)  # Increase to 1.0 or more
```

## 📧 Notifications

Configure build notifications:

### Email Notifier
- **Event**: Build failed
- **Recipients**: dev-team@company.com

### Slack Notifier (if configured)
- **Event**: Build failed
- **Channel**: #test-automation

## 🔄 Triggers

### VCS Trigger
- **Trigger Type**: VCS Trigger
- **Branch filter**: `+:refs/heads/main`
- **Trigger on**: changes in snapshot dependencies

### Schedule Trigger
- **Type**: Schedule trigger
- **Daily**: at 2:00 AM
- **Time zone**: Agent timezone
- **Branch**: main

## 📈 Build Monitoring

### Success Metrics
- All scenarios passing
- Test execution time < 5 minutes
- No agent disconnections

### Recommended Build Chain
```
1. Checkout code
2. Install dependencies
3. Run linting (optional)
4. Run BDD tests
5. Generate reports
6. Archive artifacts
```

## 🎯 Best Practices

1. **Keep agent online**: Ensure Windows agent doesn't sleep/lock
2. **Clean workspace**: Enable automatic workspace cleanup
3. **Version control**: Keep `requirements.txt` updated
4. **Test isolation**: Each scenario should be independent
5. **Logging**: Use `--format pretty` for readable console output
6. **Artifacts**: Always preserve test results and logs

## 📦 Complete Build Script Template

Here's a complete `build.bat` you can use:

```batch
@echo off
echo ================================
echo Calculator BDD Test Execution
echo ================================

REM Setup Python virtual environment
echo.
echo [1/4] Setting up Python environment...
if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo [2/4] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create results directory
echo.
echo [3/4] Preparing test execution...
if not exist "test-results" mkdir test-results
if not exist "reports" mkdir reports

REM Run tests
echo.
echo [4/4] Running BDD tests...
behave --junit --junit-directory test-results ^
       --format html --outfile reports/behave-report.html ^
       --format pretty

REM Capture exit code
set TEST_EXIT_CODE=%ERRORLEVEL%

REM Deactivate venv
call venv\Scripts\deactivate.bat

REM Exit with test result code
echo.
echo ================================
if %TEST_EXIT_CODE% EQU 0 (
    echo BUILD SUCCESSFUL
) else (
    echo BUILD FAILED
)
echo ================================
exit /b %TEST_EXIT_CODE%
```

## 🚀 Quick Start Checklist

- [ ] TeamCity agent installed on Windows machine
- [ ] Agent running as user process (not service)
- [ ] Python 3.7+ installed on agent
- [ ] Git installed on agent
- [ ] Project created in TeamCity
- [ ] VCS root configured
- [ ] Build steps configured (install deps + run tests)
- [ ] XML report processing enabled
- [ ] Artifacts configured
- [ ] Build triggered and verified

---

**Need Help?** Check TeamCity build logs for detailed error messages and Python stack traces.