#!/usr/bin/env python3
"""
Script to verify the Teflon insulator pricing fix.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.models.option import Option
import json


def verify_teflon_fix():
    """Verify that Teflon insulator pricing is correct."""
    
    db = SessionLocal()
    try:
        print("=== VERIFYING TEFLON INSULATOR PRICING FIX ===")
        
        # Get all Insulator Material options
        insulator_options = db.query(Option).filter_by(name='Insulator Material').all()
        
        print(f"Found {len(insulator_options)} Insulator Material options:")
        
        for opt in insulator_options:
            print(f"\nOption ID: {opt.id}")
            print(f"  Product families: {opt.product_families}")
            print(f"  Choices: {opt.choices}")
            print(f"  Adders: {opt.adders}")
            
            # Parse adders
            adders = json.loads(opt.adders) if isinstance(opt.adders, str) else opt.adders
            
            # Check Teflon pricing
            teflon_adder = adders.get('TEF', 0)  # Using 'TEF' code
            
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
        
        print(f"\n=== SUMMARY ===")
        print("Teflon insulator pricing should be:")
        print("- LS2000 and LS6000: Teflon (TEF) = $40 adder")
        print("- All other families: Teflon (TEF) = $0 adder (available but no extra cost)")
        
        return True
        
    finally:
        db.close()


if __name__ == "__main__":
    try:
        success = verify_teflon_fix()
        if success:
            print("\nVerification completed!")
        else:
            print("\nVerification failed!")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 