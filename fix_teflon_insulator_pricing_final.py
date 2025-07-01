#!/usr/bin/env python3
"""
Final script to fix Teflon insulator pricing structure.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.models.option import Option
import json


def fix_teflon_insulator_pricing_final():
    """Fix the Teflon insulator pricing structure for the second option."""
    
    db = SessionLocal()
    try:
        print("=== FINAL TEFLON INSULATOR PRICING FIX ===")
        
        # Find the second option (for other families)
        other_option = db.query(Option).filter(
            Option.name == 'Insulator Material',
            Option.product_families == 'LS2100,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500'
        ).first()
        
        if not other_option:
            print("ERROR: Other families option not found!")
            return False
            
        print(f"Found other families option (ID: {other_option.id})")
        print(f"Current adders: {other_option.adders}")
        
        # Fix the adders to use the correct structure
        correct_adders = {
            'TEF': 0,  # Teflon - no adder for other families
            'DEL': 0,  # Delrin - standard
            'PK': 340,  # PEEK - keep pricing
            'U': 0,  # UHMWPE - standard
            'CER': 470  # Ceramic - keep pricing
        }
        
        other_option.adders = correct_adders
        
        # Commit the changes
        db.commit()
        
        print(f"Updated adders: {correct_adders}")
        
        # Verify the fix
        print(f"\n=== VERIFICATION ===")
        all_insulator_options = db.query(Option).filter_by(name='Insulator Material').all()
        
        for opt in all_insulator_options:
            print(f"\nOption ID: {opt.id}")
            print(f"  Product families: {opt.product_families}")
            print(f"  Adders: {opt.adders}")
            
            # Check Teflon pricing
            adders_dict = json.loads(opt.adders) if isinstance(opt.adders, str) else opt.adders
            teflon_adder = adders_dict.get('TEF', 0)
            
            if "LS2000" in opt.product_families or "LS6000" in opt.product_families:
                if teflon_adder == 40:
                    print(f"  ✓ LS2000/LS6000 option has correct Teflon pricing: ${teflon_adder}")
                else:
                    print(f"  ✗ LS2000/LS6000 option has incorrect Teflon pricing: ${teflon_adder}")
            else:
                if teflon_adder == 0:
                    print(f"  ✓ Other families option has correct Teflon pricing: ${teflon_adder}")
                else:
                    print(f"  ✗ Other families option has incorrect Teflon pricing: ${teflon_adder}")
        
        print(f"\n=== FIX COMPLETE ===")
        print("Teflon insulator pricing has been corrected:")
        print("- LS2000 and LS6000: Teflon (TEF) = $40 adder")
        print("- All other families: Teflon (TEF) = $0 adder (available but no extra cost)")
        
        return True
        
    finally:
        db.close()


if __name__ == "__main__":
    try:
        success = fix_teflon_insulator_pricing_final()
        if success:
            print("\nScript completed successfully!")
        else:
            print("\nScript failed!")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 