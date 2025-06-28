#!/usr/bin/env python3
"""
Test that LS7000/2 and LS8000/2 can now be configured properly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService

def test_ls7000_2_fix():
    """Test that LS7000/2 and LS8000/2 can be configured properly"""
    print("=== TESTING LS7000/2 AND LS8000/2 FIX ===\n")
    
    db = SessionLocal()
    product_service = ProductService(db)
    config_service = ConfigurationService(db, product_service)
    
    try:
        # Test both models
        for model_name in ["LS7000/2", "LS8000/2"]:
            print(f"\n--- Testing {model_name} ---")
            
            # 1. Test getting base product
            base_product = product_service.get_base_product_for_family(db, model_name)
            if base_product:
                print(f"✓ Base product found: {base_product.get('model_number', 'Unknown')}")
            else:
                print(f"✗ No base product found")
                continue
            
            # 2. Test getting voltages
            voltages = product_service.get_available_voltages(db, model_name)
            if voltages:
                print(f"✓ Voltages found: {voltages}")
            else:
                print(f"✗ No voltages found")
                continue
            
            # 3. Test getting materials
            materials = product_service.get_available_materials_for_product(db, model_name)
            if materials:
                print(f"✓ Materials found: {len(materials)} options")
                for mat in materials:
                    choices = mat.get('choices', [])
                    if isinstance(choices, list) and len(choices) > 0:
                        material_codes = [c.get('code', c) if isinstance(c, dict) else c for c in choices]
                        print(f"  - {mat.get('name', 'Unknown')}: {material_codes}")
            else:
                print(f"✗ No materials found")
                continue
            
            # 4. Test generating a model number using the configuration service
            try:
                # Use first available voltage and material
                voltage = voltages[0] if voltages else "115VAC"
                material_choices = materials[0].get('choices', []) if materials else []
                material = material_choices[0].get('code', material_choices[0]) if material_choices else "H"
                
                # Start configuration
                config_service.start_configuration(
                    product_family_id=base_product.get('family_id', 0),
                    product_family_name=model_name,
                    base_product_info=base_product
                )
                config_service.set_option("Voltage", voltage)
                config_service.set_option("Material", material)
                config_service.set_option("Length", 10.0)
                
                model_number = config_service.generate_model_number()
                print(f"✓ Generated model number: {model_number}")
                
                # Check if the model number includes /2
                if '/2' in model_number:
                    print(f"✓ Model number correctly includes /2")
                else:
                    print(f"✗ Model number missing /2: {model_number}")
                    
            except Exception as e:
                print(f"✗ Error generating model number: {e}")
        
        print("\n=== TEST COMPLETE ===")
        
    except Exception as e:
        print(f"Error in test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()

if __name__ == "__main__":
    test_ls7000_2_fix() 