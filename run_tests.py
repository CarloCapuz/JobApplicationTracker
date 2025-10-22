#!/usr/bin/env python3
"""
Test runner script for Job Application Tracker.

This script provides convenient ways to run tests with different configurations.
"""

import subprocess
import sys
import os

def run_tests(test_type="all", verbose=True, coverage=True):
    """Run tests with specified configuration."""
    
    # Base pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add verbosity
    if verbose:
        cmd.append("-v")
    
    # Add coverage
    if coverage:
        cmd.extend(["--cov=app", "--cov-report=term-missing", "--cov-report=html:htmlcov"])
    
    # Add test type specific options
    if test_type == "unit":
        cmd.extend(["tests/test_database.py", "tests/test_api.py"])
    elif test_type == "integration":
        cmd.extend(["tests/test_summary.py"])
    elif test_type == "quick":
        cmd.extend(["-x", "--tb=short"])  # Stop on first failure, short traceback
    elif test_type == "all":
        pass  # Run all tests
    else:
        print(f"Unknown test type: {test_type}")
        return False
    
    print(f"Running tests: {test_type}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 50)
    
    # Run the tests
    result = subprocess.run(cmd)
    return result.returncode == 0

def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
    else:
        test_type = "all"
    
    success = run_tests(test_type)
    
    if success:
        print("\n[SUCCESS] All tests passed!")
        sys.exit(0)
    else:
        print("\n[FAILED] Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
