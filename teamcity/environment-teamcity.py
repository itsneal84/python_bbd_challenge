"""
Behave environment configuration - Enhanced for TeamCity
Handles before/after hooks for scenarios and features
Includes TeamCity service messages for better integration
"""
import logging
import os
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def is_running_in_teamcity():
    """Check if running in TeamCity environment"""
    return 'TEAMCITY_VERSION' in os.environ


def teamcity_message(message_name, **kwargs):
    """
    Send TeamCity service message
    https://www.jetbrains.com/help/teamcity/service-messages.html
    """
    if not is_running_in_teamcity():
        return
    
    def escape_value(s):
        """Escape special characters for TeamCity"""
        if s is None:
            return ''
        s = str(s)
        s = s.replace('|', '||')
        s = s.replace("'", "|'")
        s = s.replace('\n', '|n')
        s = s.replace('\r', '|r')
        s = s.replace('[', '|[')
        s = s.replace(']', '|]')
        return s
    
    attrs = ' '.join([f"{k}='{escape_value(v)}'" for k, v in kwargs.items()])
    print(f"##teamcity[{message_name} {attrs}]", flush=True)


def before_all(context):
    """
    Runs once before all features
    Setup any global configuration here
    """
    context.start_time = datetime.now()
    context.test_results = []
    
    print("\n" + "="*60)
    print("Starting Calculator BDD Test Suite")
    if is_running_in_teamcity():
        print("Running in TeamCity environment")
        print(f"Build Number: {os.environ.get('BUILD_NUMBER', 'N/A')}")
    print("="*60 + "\n")
    
    # TeamCity: Start test suite
    teamcity_message('testSuiteStarted', name='Calculator BDD Tests')


def before_feature(context, feature):
    """
    Runs before each feature file
    """
    print(f"\n{'='*60}")
    print(f"Feature: {feature.name}")
    print(f"{'='*60}\n")
    
    # TeamCity: Start feature suite
    teamcity_message('testSuiteStarted', name=feature.name)


def before_scenario(context, scenario):
    """
    Runs before each scenario
    """
    context.scenario_start_time = datetime.now()
    
    print(f"\nScenario: {scenario.name}")
    print("-" * 60)
    
    # TeamCity: Start test
    test_name = f"{scenario.feature.name}: {scenario.name}"
    teamcity_message('testStarted', name=test_name, captureStandardOutput='true')


def after_step(context, step):
    """
    Runs after each step
    Log step execution for better debugging
    """
    status_symbol = "✓" if step.status == "passed" else "✗"
    print(f"{status_symbol} {step.keyword} {step.name}")


def after_scenario(context, scenario):
    """
    Runs after each scenario
    Cleanup and report results
    """
    # Calculate duration
    duration = 0
    if hasattr(context, 'scenario_start_time'):
        duration = int((datetime.now() - context.scenario_start_time).total_seconds() * 1000)
    
    test_name = f"{scenario.feature.name}: {scenario.name}"
    
    # Close calculator after each scenario to ensure clean state
    if hasattr(context, 'calculator'):
        try:
            context.calculator.close()
            print("✓ Calculator closed")
        except Exception as e:
            print(f"⚠ Warning: Could not close calculator: {e}")
    
    # Handle test result
    if scenario.status == "passed":
        print(f"✓ Scenario PASSED")
        context.test_results.append({"scenario": scenario.name, "status": "PASSED"})
        
        # TeamCity: Test finished successfully
        teamcity_message('testFinished', name=test_name, duration=duration)
        
    elif scenario.status == "failed":
        print(f"✗ Scenario FAILED")
        context.test_results.append({"scenario": scenario.name, "status": "FAILED"})
        
        # Get failure details
        failure_message = "Scenario failed"
        failure_details = ""
        
        for step in scenario.steps:
            if step.status == "failed":
                failure_message = f"Step failed: {step.keyword} {step.name}"
                if step.error_message:
                    failure_details = step.error_message
                break
        
        # TeamCity: Test failed
        teamcity_message('testFailed', 
                        name=test_name, 
                        message=failure_message,
                        details=failure_details)
        teamcity_message('testFinished', name=test_name, duration=duration)
        
        # Optional: Capture screenshot on failure
        try:
            from PIL import ImageGrab
            screenshot_path = f"test-results/{scenario.name.replace(' ', '_')}_failure.png"
            screenshot = ImageGrab.grab()
            screenshot.save(screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")
            
            # TeamCity: Report artifact
            if is_running_in_teamcity():
                print(f"##teamcity[publishArtifacts '{screenshot_path}']", flush=True)
        except Exception as e:
            print(f"⚠ Could not capture screenshot: {e}")
    
    elif scenario.status == "skipped":
        print(f"⊘ Scenario SKIPPED")
        context.test_results.append({"scenario": scenario.name, "status": "SKIPPED"})
        
        # TeamCity: Test ignored
        teamcity_message('testIgnored', name=test_name, message='Scenario skipped')
        teamcity_message('testFinished', name=test_name, duration=duration)
    
    print("-" * 60)


def after_feature(context, feature):
    """
    Runs after each feature file
    """
    # TeamCity: End feature suite
    teamcity_message('testSuiteFinished', name=feature.name)


def after_all(context):
    """
    Runs once after all features
    Print final test summary
    """
    # Calculate total duration
    total_duration = 0
    if hasattr(context, 'start_time'):
        total_duration = (datetime.now() - context.start_time).total_seconds()
    
    print("\n" + "="*60)
    print("Test Suite Summary")
    print("="*60)
    
    if hasattr(context, 'test_results'):
        passed = sum(1 for r in context.test_results if r['status'] == 'PASSED')
        failed = sum(1 for r in context.test_results if r['status'] == 'FAILED')
        skipped = sum(1 for r in context.test_results if r['status'] == 'SKIPPED')
        total = len(context.test_results)
        
        print(f"\nTotal Scenarios: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Skipped: {skipped}")
        print(f"Duration: {total_duration:.2f} seconds")
        
        # TeamCity: Build statistics
        teamcity_message('buildStatisticValue', key='totalTests', value=total)
        teamcity_message('buildStatisticValue', key='passedTests', value=passed)
        teamcity_message('buildStatisticValue', key='failedTests', value=failed)
        teamcity_message('buildStatisticValue', key='ignoredTests', value=skipped)
        
        if failed == 0:
            print("\n✓ All tests passed!")
            teamcity_message('buildStatus', status='SUCCESS', text='All tests passed')
        else:
            print(f"\n✗ {failed} test(s) failed")
            print("\nFailed scenarios:")
            for result in context.test_results:
                if result['status'] == 'FAILED':
                    print(f"  - {result['scenario']}")
            
            teamcity_message('buildStatus', status='FAILURE', text=f'{failed} test(s) failed')
    
    print("\n" + "="*60 + "\n")
    
    # TeamCity: End test suite
    teamcity_message('testSuiteFinished', name='Calculator BDD Tests')