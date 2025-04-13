import pytest
import os
import sys

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)
sys.path.insert(0, os.path.join(base_dir, "app"))

print(f"Added to path: {base_dir}")
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")

if __name__ == "__main__":
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("\n=== Running utils tests ===")
    utils_test_file = os.path.join(test_dir, "tutors_availability", "test_utils.py")
    utils_result = pytest.main(["-v", utils_test_file])
    
    print("\n=== Running service tests ===")
    service_test_file = os.path.join(test_dir, "tutors_availability", "test_service.py")
    service_result = pytest.main(["-v", service_test_file])
    
    print("\n=== Running unavailability tests ===")
    unavailability_test_file = os.path.join(test_dir, "tutors_availability", "test_unavailability.py")
    unavailability_result = pytest.main(["-v", unavailability_test_file])
    
    # Return non-zero exit code if any test suite failed
    sys.exit(utils_result or service_result or unavailability_result) 
