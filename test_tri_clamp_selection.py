#!/usr/bin/env python3
"""
Test script to verify tri-clamp selection functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.models.option import Option
import json

def test_tri_clamp_selection():
    """Test the tri-clamp selection functionality."""
    
    db = SessionLocal()
    try:
        print("=== TESTING TRI-CLAMP SELECTION ===\n")
        
        # Test 1: Check that the tri-clamp option exists
        print("1. Checking tri-clamp option...")
        tri_clamp_option = db.query(Option).filter_by(name='Tri-clamp').first()
        
        if tri_clamp_option:
            print(f"   ✓ Tri-clamp option found")
            print(f"   - ID: {tri_clamp_option.id}")
            print(f"   - Category: {tri_clamp_option.category}")
            print(f"   - Product families: {tri_clamp_option.product_families}")
            
            # Parse choices and adders
            choices = json.loads(tri_clamp_option.choices) if isinstance(tri_clamp_option.choices, str) else tri_clamp_option.choices
            adders = json.loads(tri_clamp_option.adders) if isinstance(tri_clamp_option.adders, str) else tri_clamp_option.adders
            
            print(f"   - Choices: {choices}")
            print(f"   - Adders: {adders}")
            
            # Test 2: Verify the expected options exist
            print("\n2. Verifying expected tri-clamp options...")
            expected_options = [
                "1-1/2\" Tri-clamp Process Connection",
                "1-1/2\" Tri-clamp Spud", 
                "2\" Tri-clamp Process Connection",
                "2\" Tri-clamp Spud"
            ]
            
            for expected in expected_options:
                if expected in choices:
                    price = adders.get(expected, 0)
                    print(f"   ✓ {expected}: ${price}")
                else:
                    print(f"   ✗ Missing: {expected}")
            
            # Test 3: Verify pricing structure
            print("\n3. Verifying pricing structure...")
            expected_pricing = {
                "1-1/2\" Tri-clamp Process Connection": 280.0,
                "1-1/2\" Tri-clamp Spud": 170.0,
                "2\" Tri-clamp Process Connection": 330.0,
                "2\" Tri-clamp Spud": 220.0
            }
            
            for option, expected_price in expected_pricing.items():
                actual_price = adders.get(option, 0)
                if actual_price == expected_price:
                    print(f"   ✓ {option}: ${actual_price}")
                else:
                    print(f"   ✗ {option}: Expected ${expected_price}, got ${actual_price}")
            
            # Test 4: Verify UI behavior simulation
            print("\n4. Simulating UI behavior...")
            
            # Test size selection
            sizes = ["1-1/2\"", "2\""]
            for size in sizes:
                # Test process connection (no spud)
                process_connection = f"{size} Tri-clamp Process Connection"
                process_price = adders.get(process_connection, 0)
                print(f"   Size: {size}, Process Connection: ${process_price}")
                
                # Test spud version
                spud_connection = f"{size} Tri-clamp Spud"
                spud_price = adders.get(spud_connection, 0)
                print(f"   Size: {size}, Spud: ${spud_price}")
            
            print("\n=== TRI-CLAMP SELECTION TEST COMPLETE ===")
            print("The tri-clamp selection should now show:")
            print("- A 'Size' dropdown with options: 1-1/2\" and 2\"")
            print("- A 'Spud' checkbox to toggle between Process Connection and Spud")
            print("- Correct pricing for each combination")
            
        else:
            print("   ✗ Tri-clamp option not found in database")
            
    except Exception as e:
        print(f"Error testing tri-clamp selection: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_tri_clamp_selection() 