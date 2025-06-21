#!/usr/bin/env python3
"""
Test script to diagnose PerfectThemeHelper import issue
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing import of theme_helper module...")
    import src.ui.helpers.theme_helper
    print(f"SUCCESS: Module imported: {src.ui.helpers.theme_helper}")
    
    print("\nTesting import of PerfectThemeHelper class...")
    from src.ui.helpers.theme_helper import PerfectThemeHelper
    print(f"SUCCESS: PerfectThemeHelper imported: {PerfectThemeHelper}")
    
    print("\nTesting setup_main_window method...")
    print(f"Method exists: {hasattr(PerfectThemeHelper, 'setup_main_window')}")
    
except ImportError as e:
    print(f"FAILED: {e}")
except Exception as e:
    print(f"ERROR: {e}")

print("\nTest completed.") 