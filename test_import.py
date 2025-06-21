#!/usr/bin/env python3
"""
Test script to verify import of fix_configuration_dialog_layout
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing direct import from window_layout_helper...")
    from src.ui.helpers.window_layout_helper import fix_configuration_dialog_layout
    print(f"SUCCESS: Imported {fix_configuration_dialog_layout}")
    print(f"Function name: {fix_configuration_dialog_layout.__name__}")
    print(f"Function doc: {fix_configuration_dialog_layout.__doc__}")
except ImportError as e:
    print(f"FAILED: {e}")
    
try:
    print("\nTesting import through helpers module...")
    from src.ui.helpers import fix_configuration_dialog_layout
    print(f"SUCCESS: Imported {fix_configuration_dialog_layout}")
except ImportError as e:
    print(f"FAILED: {e}")

print("\nTest completed.") 