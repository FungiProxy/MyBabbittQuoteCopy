#!/usr/bin/env python3
"""
Check the current database structure for exotic metals.
"""

import sys
import os
sys.path.append(os.path.abspath('.'))

from src.core.database import SessionLocal
from src.core.models.option import Option

def check_exotic_metals_in_db():
    """Check if exotic metals are properly configured in the database."""
    db = SessionLocal()
    try:
        print("Checking exotic metals configuration in database...")
        
        # Get all material options
        material_options = db.query(Option).filter(
            Option.name == "Material",
            Option.category == "Material"
        ).all()
        
        print(f"\nFound {len(material_options)} material options:")
        
        # Collect all exotic metal codes found
        all_exotic_codes = set()
        
        for option in material_options:
            print(f"\nProduct Family: {option.product_families}")
            
            # Check if choices is a list of dicts or strings
            choices_list = option.choices if isinstance(option.choices, list) else []
            adders_dict = option.adders if isinstance(option.adders, dict) else {}
            
            # Extract codes from choices
            codes = []
            for choice in choices_list:
                if isinstance(choice, dict):
                    code = choice.get('code', '')
                    display_name = choice.get('display_name', '')
                    codes.append(code)
                    # Check if this looks like an exotic metal
                    if any(exotic in display_name.lower() for exotic in ['alloy', 'hastelloy', 'titanium', 'monel', 'inconel']):
                        all_exotic_codes.add(code)
                else:
                    codes.append(str(choice))
            
            print(f"  Codes: {codes}")
            
            # Show exotic metals specifically
            exotic_in_family = [code for code in codes if code in all_exotic_codes]
            if exotic_in_family:
                print(f"  Exotic metals in this family: {exotic_in_family}")
                for exotic in exotic_in_family:
                    adder = adders_dict.get(exotic, 0)
                    print(f"    {exotic}: ${adder}")
        
        print(f"\n" + "="*60)
        print(f"ALL EXOTIC METAL CODES FOUND: {sorted(all_exotic_codes)}")
        print("="*60)
        
        # Show what we think are exotic metals
        print("\nExotic metal codes identified:")
        for code in sorted(all_exotic_codes):
            print(f"  - {code}")
        
        print("\nDatabase check complete!")
        
    except Exception as e:
        print(f"Error checking database: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_exotic_metals_in_db() 