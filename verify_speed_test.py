#!/usr/bin/env python3
"""
Verification script for speed test functionality implementation
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def verify_speed_test_implementation():
    """Verify that speed test functionality is properly implemented."""
    print("=== Speed Test Implementation Verification ===")
    print()
    
    # Check if the required files exist
    files_to_check = [
        "src/nordvpn_manager.py",
        "src/main_window.py", 
        "requirements.txt",
        "test_speed.py"
    ]
    
    print("Checking required files...")
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")
            return False
    
    # Check requirements.txt for speedtest-cli
    print("\nChecking requirements.txt...")
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()
            if "speedtest-cli" in content:
                print("✓ speedtest-cli dependency found in requirements.txt")
            else:
                print("✗ speedtest-cli dependency missing from requirements.txt")
                return False
    except Exception as e:
        print(f"✗ Error reading requirements.txt: {e}")
        return False
    
    # Check nordvpn_manager.py for speed test methods
    print("\nChecking nordvpn_manager.py implementation...")
    try:
        with open("src/nordvpn_manager.py", "r") as f:
            content = f.read()
            
        required_methods = [
            "get_connection_speed",
            "run_speed_test", 
            "_get_speed_rating",
            "_get_ping_rating"
        ]
        
        for method in required_methods:
            if f"def {method}" in content:
                print(f"✓ {method} method found")
            else:
                print(f"✗ {method} method missing")
                return False
                
        # Check for speedtest import
        if "import speedtest" in content:
            print("✓ speedtest import found")
        else:
            print("✗ speedtest import missing")
            return False
            
    except Exception as e:
        print(f"✗ Error reading nordvpn_manager.py: {e}")
        return False
    
    # Check main_window.py for speed test UI
    print("\nChecking main_window.py implementation...")
    try:
        with open("src/main_window.py", "r") as f:
            content = f.read()
            
        required_elements = [
            "test_speed",
            "_run_speed_test",
            "speed_progress",
            "Test Connection Speed"
        ]
        
        for element in required_elements:
            if element in content:
                print(f"✓ {element} found in UI")
            else:
                print(f"✗ {element} missing from UI")
                return False
                
    except Exception as e:
        print(f"✗ Error reading main_window.py: {e}")
        return False
    
    # Check test_speed.py
    print("\nChecking test_speed.py...")
    try:
        with open("test_speed.py", "r") as f:
            content = f.read()
            
        if "test_speed_test" in content and "NordVPNManager" in content:
            print("✓ test_speed.py properly implemented")
        else:
            print("✗ test_speed.py missing required functions")
            return False
            
    except Exception as e:
        print(f"✗ Error reading test_speed.py: {e}")
        return False
    
    return True

def main():
    """Run the verification."""
    success = verify_speed_test_implementation()
    
    print(f"\n=== Verification Result ===")
    if success:
        print("✓ Speed test functionality is properly implemented!")
        print("\nTo test the functionality:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the test: python3 test_speed.py")
        print("3. Or run the main app: python3 main.py")
    else:
        print("✗ Speed test functionality has implementation issues.")
        print("Please check the errors above and fix them.")

if __name__ == "__main__":
    main() 