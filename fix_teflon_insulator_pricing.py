#!/usr/bin/env python3
"""
Script to fix Teflon insulator pricing.
Teflon insulator should only be a price adder for LS2000 and LS6000,
but should remain available for all models.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.models.option import Option


def fix_teflon_insulator_pricing():
    """Fix Teflon insulator pricing to only apply adders for LS2000 and LS6000."""
    
    db = SessionLocal()
    try:
        print("=== FIXING TEFLON INSULATOR PRICING ===")
        
        # Find the current Insulator Material option
        insulator_option = db.query(Option).filter_by(name='Insulator Material').first()
        
        if not insulator_option:
            print("ERROR: Insulator Material option not found!")
            return False
            
        print(f"Found Insulator Material option (ID: {insulator_option.id})")
        print(f"Current product families: {insulator_option.product_families}")
        print(f"Current choices: {insulator_option.choices}")
        print(f"Current adders: {insulator_option.adders}")
        
        # Parse the current choices and adders
        import json
        choices = json.loads(insulator_option.choices) if isinstance(insulator_option.choices, str) else insulator_option.choices
        adders = json.loads(insulator_option.adders) if isinstance(insulator_option.adders, str) else insulator_option.adders
        
        print(f"\nCurrent choices: {choices}")
        print(f"Current adders: {adders}")
        
        # Create separate options for LS2000/LS6000 (with pricing) and other families (without pricing)
        
        # 1. Update the existing option to only apply to LS2000 and LS6000 (with pricing)
        ls2000_ls6000_families = "LS2000,LS6000"
        insulator_option.product_families = ls2000_ls6000_families
        
        # Keep the current adders (Teflon Upgrade: 40, PEEK: 340, Ceramic: 470)
        # The adders are already correct for LS2000/LS6000
        print(f"\nUpdated existing option for LS2000/LS6000:")
        print(f"  Product families: {insulator_option.product_families}")
        print(f"  Adders: {adders}")
        
        # 2. Create a new option for other families without Teflon pricing
        other_families = "LS2100,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500"
        
        # Create adders without Teflon pricing
        other_adders = {
            "Standard": 0,
            "Teflon Upgrade": 0,  # No adder for other families
            "PEEK": 340,  # Keep PEEK pricing
            "Ceramic": 470  # Keep Ceramic pricing
        }
        
        # Check if option already exists for other families
        existing_other = db.query(Option).filter(
            Option.name == 'Insulator Material',
            Option.product_families == other_families
        ).first()
        
        if existing_other:
            print(f"\nUpdating existing option for other families (ID: {existing_other.id})")
            existing_other.adders = other_adders
        else:
            print(f"\nCreating new option for other families")
            new_option = Option(
                name="Insulator Material",
                description="Insulator material selection (standard vs optional materials) - No Teflon pricing",
                price=0.0,
                price_type="fixed",
                category="Connections",
                product_families=other_families,
                choices=choices,
                adders=other_adders,
                rules=None
            )
            db.add(new_option)
            print(f"  Created new option with ID: {new_option.id}")
        
        # Commit the changes
        db.commit()
        
        print(f"\n=== VERIFICATION ===")
    finally:
        db.close()
        
        # Verify the changes
        all_insulator_options = db.query(Option).filter_by(name='Insulator Material').all()
        print(f"Total Insulator Material options: {len(all_insulator_options)}")
        
        for opt in all_insulator_options:
            print(f"\nOption ID: {opt.id}")
            print(f"  Product families: {opt.product_families}")
            print(f"  Adders: {opt.adders}")
            
            # Check if Teflon pricing is correct
            adders_dict = json.loads(opt.adders) if isinstance(opt.adders, str) else opt.adders
            teflon_adder = adders_dict.get("Teflon Upgrade", 0)
            
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
        print("Teflon insulator pricing has been updated:")
        print("- LS2000 and LS6000: Teflon Upgrade = $40 adder")
        print("- All other families: Teflon Upgrade = $0 adder (available but no extra cost)")
        
        return True


if __name__ == "__main__":
    try:
        success = fix_teflon_insulator_pricing()
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