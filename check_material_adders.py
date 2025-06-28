#!/usr/bin/env python3
"""
Check material adders and pricing logic
"""

import json
from src.core.database import engine, SessionLocal
from src.core.services.product_service import ProductService
from sqlalchemy import text

def check_material_adders():
    """Check current material adders and pricing"""
    try:
        print("=== CHECKING MATERIAL ADDERS ===")
        
        # Check database values
        with engine.connect() as conn:
            print("\n1. Current material adders in database:")
            result = conn.execute(text("SELECT id, name, choices, adders, product_families FROM options WHERE name = 'Material'"))
            rows = result.fetchall()
            
            for row in rows:
                option_id, name, choices, adders, product_families = row
                print(f"\nMaterial option ID {option_id} for families: {product_families}")
                
                try:
                    choices_data = json.loads(choices) if choices else []
                    adders_data = json.loads(adders) if adders else {}
                    
                    print(f"  Choices: {choices_data}")
                    print(f"  Adders: {adders_data}")
                    
                    # Check specific materials
                    for choice in choices_data:
                        if isinstance(choice, dict) and 'code' in choice:
                            code = choice['code']
                            display_name = choice.get('display_name', 'Unknown')
                            adder = adders_data.get(code, 0)
                            print(f"    {code} ({display_name}): ${adder}")
                    
                except json.JSONDecodeError as e:
                    print(f"  ✗ JSON decode error: {e}")
        
        # Test pricing logic
        print("\n2. Testing pricing logic:")
        db = SessionLocal()
        product_service = ProductService(db)
        
        # Test for LS2000
        test_family = "LS2000"
        print(f"\nTesting pricing for {test_family}:")
        
        # Get available materials
        materials = product_service.get_available_materials_for_product(db, test_family)
        print(f"Available materials: {materials}")
        
        if materials:
            material_option = materials[0]
            choices = material_option.get('choices', [])
            adders = material_option.get('adders', {})
            
            print(f"Material choices: {choices}")
            print(f"Material adders: {adders}")
            
            # Test length adder calculation
            print(f"\nTesting length adders for U and T:")
            for material_code in ['U', 'T']:
                for length in [24, 36, 48]:
                    try:
                        length_adder = product_service.calculate_length_price(test_family, material_code, length)
                        print(f"  {material_code} at {length}\": ${length_adder:.2f}")
                    except Exception as e:
                        print(f"  {material_code} at {length}\": Error - {e}")
        
        db.close()
        
    except Exception as e:
        print(f"Error checking material adders: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_material_adders() 