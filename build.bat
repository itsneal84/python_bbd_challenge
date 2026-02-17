@echo off
REM ================================
REM Calculator BDD Test Build Script
REM For TeamCity Execution
REM ================================

echo.
echo ================================
echo Calculator BDD Test Execution
echo ================================
echo Build Number: %BUILD_NUMBER%
echo.

REM Exit on error
setlocal EnableDelayedExpansion

REM Setup Python virtual environment
echo [1/5] Setting up Python environment...
if not exist "venv" (
    echo Creating new virtual environment...
    python -m venv venv
    if !ERRORLEVEL! NEQ 0 (
        echo ERROR: Failed to create virtual environment
        exit /b 1
    )
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if !ERRORLEVEL! NEQ 0 (
    echo ERROR: Failed to activate virtual environment
    exit /b 1
)

REM Verify Python
echo Verifying Python installation...
python --version
pip --version

REM Install/upgrade dependencies
echo.
echo [2/5] Installing dependencies...
python -m pip install --upgrade pip
if !ERRORLEVEL! NEQ 0 (
    echo ERROR: Failed to upgrade pip
    exit /b 1
)

pip install -r requirements.txt
if !ERRORLEVEL! NEQ 0 (
    echo ERROR: Failed to install requirements
    exit /b 1
)

echo Installed packages:
pip list

REM Create results directories
echo.
echo [3/5] Preparing test execution...
if not exist "test-results" mkdir test-results
if not exist "reports" mkdir reports
echo Test results directory: %CD%\test-results
echo Reports directory: %CD%\reports

REM Check if Calculator is available
echo.
echo [4/5] Verifying Windows Calculator availability...
where calc.exe >nul 2>&1
if !ERRORLEVEL! NEQ 0 (
    echo WARNING: calc.exe not found in PATH
    echo Attempting to locate Calculator...
    if exist "C:\Windows\System32\calc.exe" (
        echo Found: C:\Windows\System32\calc.exe
    ) else (
        echo ERROR: Windows Calculator not found
        exit /b 1
    )
) else (
    echo Windows Calculator found in PATH
)

REM Run BDD tests
echo.
echo [5/5] Running BDD tests...
echo ================================
echo.

behave --junit --junit-directory test-results --format html --outfile reports/behave-report.html --format pretty --no-capture

REM Capture exit code
set TEST_EXIT_CODE=!ERRORLEVEL!

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat

REM Display results
echo.
echo ================================
echo Test Execution Complete
echo ================================
echo.

if exist "test-results\*.xml" (
    echo JUnit XML reports generated in: test-results\
    dir /b test-results\*.xml
) else (
    echo WARNING: No JUnit XML reports found
)

echo.
if exist "reports\behave-report.html" (
    echo HTML report generated: reports\behave-report.html
) else (
    echo WARNING: No HTML report found
)

echo.
echo ================================
if !TEST_EXIT_CODE! EQU 0 (
    echo ##teamcity[buildStatus status='SUCCESS' text='All tests passed']
    echo BUILD SUCCESSFUL - All tests passed
    echo Exit Code: 0
) else (
    echo ##teamcity[buildStatus status='FAILURE' text='Tests failed']
    echo BUILD FAILED - Some tests failed
    echo Exit Code: !TEST_EXIT_CODE!
)
echo ================================

REM Exit with the test result code
exit /b !TEST_EXIT_CODE!