#!/usr/bin/env python3
"""
Test script for PyNord application
This script tests the basic functionality without requiring NordVPN CLI
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        from nordvpn_manager import NordVPNManager
        print("✓ NordVPNManager imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import NordVPNManager: {e}")
        return False
    
    try:
        from main_window import MainWindow
        print("✓ MainWindow imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import MainWindow: {e}")
        return False
    
    return True

def test_vpn_manager():
    """Test VPN manager functionality."""
    print("\nTesting VPN Manager...")
    
    try:
        from nordvpn_manager import NordVPNManager
        manager = NordVPNManager()
        
        # Test basic methods
        status = manager.get_status()
        print(f"✓ Status check: {status}")
        
        # Test if NordVPN is installed
        installed = manager.is_nordvpn_installed()
        print(f"✓ NordVPN CLI check: {'Installed' if installed else 'Not installed'}")
        
        return True
    except Exception as e:
        print(f"✗ VPN Manager test failed: {e}")
        return False

def test_gui_imports():
    """Test GUI-related imports."""
    print("\nTesting GUI imports...")
    
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox
        print("✓ Tkinter imports successful")
        return True
    except ImportError as e:
        print(f"✗ Tkinter import failed: {e}")
        print("  Tkinter should be included with Python by default")
        return False

def main():
    """Run all tests."""
    print("=== PyNord Application Test ===")
    print()
    
    tests_passed = 0
    total_tests = 3
    
    # Test imports
    if test_imports():
        tests_passed += 1
    
    # Test VPN manager
    if test_vpn_manager():
        tests_passed += 1
    
    # Test GUI imports
    if test_gui_imports():
        tests_passed += 1
    
    print(f"\n=== Test Results ===")
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("✓ All tests passed! The application should work correctly.")
        print("\nTo run the application:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run: python main.py")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("- Tkinter should be included with Python by default")
        print("- Install NordVPN CLI for full functionality")
        print("- Check Python version (3.8+ required)")

if __name__ == "__main__":
    main() 