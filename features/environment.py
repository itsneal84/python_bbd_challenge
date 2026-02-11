"""
Behave environment configuration
Handles before/after hooks for scenarios and features
"""
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def before_all(context):
    """
    Runs once before all features
    Setup any global configuration here
    """
    print("\n" + "="*60)
    print("Starting Calculator BDD Test Suite")
    print("="*60 + "\n")
    context.test_results = []


def before_feature(context, feature):
    """
    Runs before each feature file
    """
    print(f"\n{'='*60}")
    print(f"Feature: {feature.name}")
    print(f"{'='*60}\n")


def before_scenario(context, scenario):
    """
    Runs before each scenario
    """
    print(f"\nScenario: {scenario.name}")
    print("-" * 60)


def after_scenario(context, scenario):
    """
    Runs after each scenario
    Cleanup: close calculator if it's still open
    """
    # Close calculator after each scenario to ensure clean state
    if hasattr(context, 'calculator'):
        try:
            context.calculator.close()
            print("✓ Calculator closed")
        except Exception as e:
            print(f"⚠ Warning: Could not close calculator: {e}")
    
    # Print scenario result
    if scenario.status == "passed":
        print(f"✓ Scenario PASSED")
        context.test_results.append({"scenario": scenario.name, "status": "PASSED"})
    else:
        print(f"✗ Scenario FAILED")
        context.test_results.append({"scenario": scenario.name, "status": "FAILED"})
    
    print("-" * 60)


def after_feature(context, feature):
    """
    Runs after each feature file
    """
    pass


def after_all(context):
    """
    Runs once after all features
    Print final test summary
    """
    print("\n" + "="*60)
    print("Test Suite Summary")
    print("="*60)
    
    if hasattr(context, 'test_results'):
        passed = sum(1 for r in context.test_results if r['status'] == 'PASSED')
        failed = sum(1 for r in context.test_results if r['status'] == 'FAILED')
        total = len(context.test_results)
        
        print(f"\nTotal Scenarios: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        
        if failed == 0:
            print("\n✓ All tests passed!")
        else:
            print(f"\n✗ {failed} test(s) failed")
            print("\nFailed scenarios:")
            for result in context.test_results:
                if result['status'] == 'FAILED':
                    print(f"  - {result['scenario']}")
    
    print("\n" + "="*60 + "\n")