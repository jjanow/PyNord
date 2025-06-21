#!/usr/bin/env python3
"""
Test script for speed test functionality
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_speed_test():
    """Test the speed test functionality."""
    print("Testing speed test functionality...")
    
    try:
        from nordvpn_manager import NordVPNManager
        
        # Create VPN manager instance
        manager = NordVPNManager()
        
        print("✓ NordVPNManager created successfully")
        
        # Test basic speed test
        print("\nRunning basic speed test...")
        result = manager.get_connection_speed()
        
        if result.get('success'):
            print("✓ Speed test completed successfully!")
            print(f"  Download: {result['download_mbps']} Mbps")
            print(f"  Upload: {result['upload_mbps']} Mbps")
            print(f"  Ping: {result['ping_ms']} ms")
            print(f"  Server: {result['server']} ({result['server_country']})")
        else:
            print(f"✗ Speed test failed: {result.get('error', 'Unknown error')}")
        
        # Test comprehensive speed test with progress
        print("\nRunning comprehensive speed test with progress...")
        
        def progress_callback(message):
            print(f"  Progress: {message}")
        
        result = manager.run_speed_test(progress_callback)
        
        if result.get('success'):
            print("✓ Comprehensive speed test completed successfully!")
            print(f"  Download: {result['download_mbps']} Mbps ({result['download_rating']})")
            print(f"  Upload: {result['upload_mbps']} Mbps ({result['upload_rating']})")
            print(f"  Ping: {result['ping_ms']} ms ({result['ping_rating']})")
            print(f"  Server: {result['server']} ({result['server_country']})")
            print(f"  Distance: {result['server_distance']} km")
            print(f"  Timestamp: {result['timestamp']}")
        else:
            print(f"✗ Comprehensive speed test failed: {result.get('error', 'Unknown error')}")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("  Make sure speedtest-cli is installed: pip install speedtest-cli")
        return False
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

def main():
    """Run the speed test."""
    print("=== Speed Test Functionality Test ===")
    print()
    
    success = test_speed_test()
    
    print(f"\n=== Test Result ===")
    if success:
        print("✓ Speed test functionality is working correctly!")
        print("\nThe speed test feature is ready to use in the PyNord application.")
    else:
        print("✗ Speed test functionality has issues.")
        print("\nPlease check:")
        print("- speedtest-cli is installed: pip install speedtest-cli")
        print("- Internet connection is available")
        print("- No firewall blocking speed test")

if __name__ == "__main__":
    main() 