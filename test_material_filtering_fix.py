#!/usr/bin/env python3
"""
Test script to verify that material filtering is now working correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService


def test_material_filtering():
    """Test material filtering for different product families."""
    print("=== TESTING MATERIAL FILTERING FIX ===\n")
    
    db = SessionLocal()
    product_service = ProductService(db)
    
    # Test families that should have different materials
    test_families = [
        "LS2000",   # Should have all materials
        "LS6000",   # Should have CPVC
        "LS7000",   # Should have CPVC  
        "LS7000/2", # Should have limited materials
        "FS10000",  # Should have limited materials
        "LT9000"    # Should have limited materials
    ]
    
    for family_name in test_families:
        print(f"--- {family_name} ---")
        
        # Get materials for this family
        materials = product_service.get_available_materials_for_product(db, family_name)
        print(f"Material options returned: {len(materials)}")
        
        for i, material in enumerate(materials):
            print(f"  Material Option {i+1}:")
            print(f"    Name: {material.get('name', 'Unknown')}")
            
            choices = material.get('choices', [])
            if choices:
                # Extract material codes
                material_codes = []
                for choice in choices:
                    if isinstance(choice, dict):
                        material_codes.append(choice.get('code', 'Unknown'))
                    else:
                        material_codes.append(str(choice))
                
                print(f"    Available materials: {material_codes}")
                
                # Check for CPVC specifically
                if any('CPVC' in code for code in material_codes):
                    print(f"    ✓ CPVC is available")
                else:
                    print(f"    ✗ CPVC is NOT available")
            else:
                print(f"    No choices defined")
            
            adders = material.get('adders', {})
            if adders:
                print(f"    Material adders: {adders}")
        
        print()
    
    db.close()
    print("=== TEST COMPLETE ===")


if __name__ == "__main__":
    test_material_filtering() 