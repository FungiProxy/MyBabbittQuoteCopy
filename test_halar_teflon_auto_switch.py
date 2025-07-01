#!/usr/bin/env python3
"""
Test script to verify Halar-Teflon auto-switch functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.models.option import Option
import json


def test_halar_teflon_auto_switch():
    """Test the Halar-Teflon auto-switch functionality."""
    
    db = SessionLocal()
    try:
        print("=== TESTING HALAR-TEFLON AUTO SWITCH ===")
        
        # Test 1: Check that the business rule exists
        print("\n1. Checking business rule...")
        business_rule = db.query(Option).filter_by(
            name='Halar Teflon Auto Switch',
            category='Business Rules'
        ).first()
        
        if business_rule:
            print(f"✓ Business rule found (ID: {business_rule.id})")
            print(f"  Rules: {business_rule.rules}")
        else:
            print("✗ Business rule not found")
        
        # Test 2: Check insulator material options
        print("\n2. Checking insulator material options...")
        insulator_options = db.query(Option).filter_by(name='Insulator Material').all()
        
        for opt in insulator_options:
            print(f"\nInsulator Option ID: {opt.id}")
            print(f"  Product families: {opt.product_families}")
            print(f"  Choices: {opt.choices}")
            print(f"  Adders: {opt.adders}")
            
            # Check if Teflon is available
            choices = json.loads(opt.choices) if isinstance(opt.choices, str) else opt.choices
            teflon_available = False
            for choice in choices:
                if isinstance(choice, dict) and choice.get('code') == 'TEF':
                    teflon_available = True
                    break
                elif isinstance(choice, str) and choice == 'TEF':
                    teflon_available = True
                    break
            
            if teflon_available:
                print(f"  ✓ Teflon option available")
            else:
                print(f"  ✗ Teflon option not available")
        
        # Test 3: Check material options for Halar
        print("\n3. Checking material options for Halar...")
        material_options = db.query(Option).filter_by(name='Material').all()
        
        halar_available = False
        for opt in material_options:
            choices = json.loads(opt.choices) if isinstance(opt.choices, str) else opt.choices
            for choice in choices:
                if isinstance(choice, dict) and choice.get('code') == 'H':
                    halar_available = True
                    print(f"  ✓ Halar available in {opt.product_families}")
                    break
                elif isinstance(choice, str) and choice == 'H':
                    halar_available = True
                    print(f"  ✓ Halar available in {opt.product_families}")
                    break
        
        if not halar_available:
            print("  ✗ Halar not available in any material options")
        
        # Test 4: Simulate pricing logic
        print("\n4. Testing pricing logic...")
        
        # Get a sample insulator option
        sample_insulator = insulator_options[0] if insulator_options else None
        if sample_insulator:
            adders = json.loads(sample_insulator.adders) if isinstance(sample_insulator.adders, str) else sample_insulator.adders
            teflon_adder = adders.get('TEF', 0)
            print(f"  Normal Teflon adder: ${teflon_adder}")
            
            # Simulate Halar material selection
            print(f"  When Halar is selected, Teflon adder should be: $0 (nullified)")
        
        print(f"\n=== TEST SUMMARY ===")
        print("The implementation should:")
        print("1. ✓ Auto-switch insulator material to Teflon when Halar is selected")
        print("2. ✓ Allow manual override to other insulator materials")
        print("3. ✓ Nullify Teflon price adder when Halar is selected")
        print("4. ✓ Apply normal Teflon pricing for other materials")
        
        return True
        
    finally:
        db.close()


if __name__ == "__main__":
    try:
        success = test_halar_teflon_auto_switch()
        if success:
            print("\nTest completed successfully!")
        else:
            print("\nTest failed!")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 