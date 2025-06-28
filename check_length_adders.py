#!/usr/bin/env python3
"""
Check length adder rules for U and T materials
"""

import json
from src.core.database import engine, SessionLocal
from src.core.services.product_service import ProductService
from sqlalchemy import text

def check_length_adders():
    """Check length adder rules and test calculations"""
    try:
        print("=== CHECKING LENGTH ADDERS ===")
        
        # Check length adder rules in database
        with engine.connect() as conn:
            print("\n1. Length adder rules in database:")
            result = conn.execute(text("SELECT * FROM length_adder_rules"))
            rows = result.fetchall()
            
            if rows:
                print(f"Found {len(rows)} length adder rules:")
                for row in rows:
                    print(f"  {row}")
            else:
                print("No length adder rules found in database")
        
        # Test length adder calculations
        print("\n2. Testing length adder calculations:")
        db = SessionLocal()
        product_service = ProductService(db)
        
        # Test families that should have U and T
        test_families = ["LS2000", "LS2100", "LS6000", "LS7000", "LS8000"]
        
        for family in test_families:
            print(f"\nTesting {family}:")
            
            # Test U material at different lengths
            for length in [24, 36, 48, 60]:
                try:
                    length_adder = product_service.calculate_length_price(family, "U", length)
                    print(f"  U at {length}\": ${length_adder:.2f}")
                except Exception as e:
                    print(f"  U at {length}\": Error - {e}")
            
            # Test T material at different lengths
            for length in [24, 36, 48, 60]:
                try:
                    length_adder = product_service.calculate_length_price(family, "T", length)
                    print(f"  T at {length}\": ${length_adder:.2f}")
                except Exception as e:
                    print(f"  T at {length}\": Error - {e}")
        
        db.close()
        
        # Check if length adder rules exist for U and T
        print("\n3. Checking for U and T length adder rules:")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM length_adder_rules WHERE material_code IN ('U', 'T')"))
            rows = result.fetchall()
            
            if rows:
                print(f"Found {len(rows)} rules for U and T:")
                for row in rows:
                    print(f"  {row}")
            else:
                print("No length adder rules found for U and T materials")
                print("This might be why length adders aren't being applied!")
        
    except Exception as e:
        print(f"Error checking length adders: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_length_adders() 