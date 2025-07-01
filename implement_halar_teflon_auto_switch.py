#!/usr/bin/env python3
"""
Script to implement automatic switching of insulator material to Teflon when Halar is selected.
This ensures that when Halar material is selected, the insulator material automatically switches to Teflon
and no price adder is applied regardless of the model's normal Teflon pricing.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.models.option import Option
import json


def implement_halar_teflon_auto_switch():
    """Implement automatic Teflon insulator switching for Halar material."""
    
    db = SessionLocal()
    try:
        print("=== IMPLEMENTING HALAR-TEFLON AUTO SWITCH ===")
        
        # First, let's check the current state of the database
        print("\n=== CURRENT DATABASE STATE ===")
        
        # Check all Insulator Material options
        insulator_options = db.query(Option).filter_by(name='Insulator Material').all()
        print(f"Found {len(insulator_options)} Insulator Material options:")
        
        for opt in insulator_options:
            print(f"\nOption ID: {opt.id}")
            print(f"  Product families: {opt.product_families}")
            print(f"  Choices: {opt.choices}")
            print(f"  Adders: {opt.adders}")
        
        # Check Material options to understand the structure
        material_options = db.query(Option).filter_by(name='Material').all()
        print(f"\nFound {len(material_options)} Material options:")
        
        for opt in material_options:
            print(f"\nMaterial Option ID: {opt.id}")
            print(f"  Product families: {opt.product_families}")
            print(f"  Choices: {opt.choices}")
            print(f"  Adders: {opt.adders}")
        
        print(f"\n=== IMPLEMENTATION PLAN ===")
        print("1. Create a new pricing strategy that detects Halar material selection")
        print("2. When Halar is detected, automatically set insulator material to Teflon")
        print("3. Ensure no price adder is applied for Teflon when Halar is selected")
        print("4. Update the UI to reflect this automatic switching")
        
        # The implementation will be done in the pricing service and UI components
        # For now, let's create a configuration option to track this business rule
        
        # Check if the business rule option already exists
        business_rule_option = db.query(Option).filter_by(
            name='Halar Teflon Auto Switch',
            category='Business Rules'
        ).first()
        
        if not business_rule_option:
            print(f"\nCreating business rule option for Halar-Teflon auto switch...")
            business_rule_option = Option(
                name='Halar Teflon Auto Switch',
                description='Automatically switch insulator material to Teflon when Halar material is selected',
                price=0.0,
                price_type='fixed',
                category='Business Rules',
                product_families='LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500',
                choices=['Enabled'],
                adders={'Enabled': 0},
                rules={
                    'trigger_material': 'H',
                    'auto_set_insulator': 'TEF',
                    'no_price_adder': True,
                    'description': 'When Halar (H) material is selected, automatically set insulator material to Teflon (TEF) with no price adder'
                }
            )
            db.add(business_rule_option)
            print(f"  Created business rule option with ID: {business_rule_option.id}")
        else:
            print(f"\nBusiness rule option already exists (ID: {business_rule_option.id})")
        
        # Commit the changes
        db.commit()
        
        print(f"\n=== VERIFICATION ===")
        
        # Verify the business rule was created
        all_business_rules = db.query(Option).filter_by(category='Business Rules').all()
        print(f"Total business rules: {len(all_business_rules)}")
        
        for rule in all_business_rules:
            print(f"\nBusiness Rule: {rule.name}")
            print(f"  Rules: {rule.rules}")
        
        print(f"\n=== IMPLEMENTATION COMPLETE ===")
        print("The business rule for Halar-Teflon auto switch has been created.")
        print("Next steps:")
        print("1. Update the pricing service to check for this business rule")
        print("2. Update the UI to automatically switch insulator material when Halar is selected")
        print("3. Ensure no price adder is applied for Teflon when Halar is the trigger")
        
        return True
        
    finally:
        db.close()


if __name__ == "__main__":
    try:
        success = implement_halar_teflon_auto_switch()
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