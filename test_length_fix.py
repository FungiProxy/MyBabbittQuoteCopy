#!/usr/bin/env python3
"""
Quick test to verify the length adder fix.
"""

import sys
import os
sys.path.append(os.path.abspath('.'))

from src.core.services.product_service import ProductService
from src.core.database import get_db

def test_length_fix():
    """Test the length adder fix."""
    db = next(get_db())
    product_service = ProductService(db)
    
    print("Testing Length Adder Fix")
    print("=" * 40)
    
    # Test LS2000 S material specifically
    test_cases = [
        (24, 0.0, "24\" - at threshold, no adder"),
        (25, 45.0, "25\" - 1 inch beyond, should have 1 foot adder"),
        (36, 45.0, "36\" - exactly 1 foot beyond, should have 1 foot adder"),
        (37, 45.0, "37\" - 1 inch into second foot, should have 1 foot adder"),
        (48, 90.0, "48\" - exactly 2 feet beyond, should have 2 foot adder"),
        (49, 90.0, "49\" - 1 inch into third foot, should have 2 foot adder"),
    ]
    
    for length, expected, description in test_cases:
        actual = product_service.calculate_length_price("LS2000", "S", length)
        status = "✓" if abs(actual - expected) < 0.01 else "✗"
        print(f"{status} {description}")
        print(f"   Expected: ${expected:.2f}, Actual: ${actual:.2f}")
        if abs(actual - expected) >= 0.01:
            print(f"   ❌ Mismatch!")
        print()

if __name__ == "__main__":
    test_length_fix() 