#!/usr/bin/env python3

import pytest
import os
import sys

# Add parent directory and app directory to path so that we can import modules
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)
sys.path.insert(0, os.path.join(base_dir, "app"))

print(f"Added to path: {base_dir}")
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")

if __name__ == "__main__":
    # Get test directory
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Run the unit tests
    print("\n=== Running unit tests ===")
    unit_test_file = os.path.join(test_dir, "tutors_availability", "test_utils.py")
    unit_result = pytest.main(["-v", unit_test_file])
    
    # Return the result (0 is success, anything else is failure)
    sys.exit(unit_result) 