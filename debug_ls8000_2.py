#!/usr/bin/env python3
"""
Debug script to test LS8000/2 specifically
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService

def main():
    """Test LS8000/2 specifically"""
    db = SessionLocal()
    product_service = ProductService(db)
    
    try:
        print("=== TESTING LS8000/2 SPECIFICALLY ===")
        
        model_name = "LS8000/2"
        
        # Test getting base product info
        print(f"\n--- Testing base product for {model_name} ---")
        base_product = product_service.get_base_product_for_family(db, model_name)
        if base_product:
            print(f"✓ Base product found for {model_name}: {base_product}")
        else:
            print(f"✗ No base product found for {model_name}")
        
        # Test getting available materials
        print(f"\n--- Testing materials for {model_name} ---")
        materials = product_service.get_available_materials_for_product(db, model_name)
        if materials:
            print(f"✓ Materials found for {model_name}: {len(materials)} options")
            for mat in materials:
                print(f"  - {mat.get('name', 'Unknown')}: {mat.get('choices', [])}")
        else:
            print(f"✗ No materials found for {model_name}")
        
        # Test getting available voltages
        print(f"\n--- Testing voltages for {model_name} ---")
        voltages = product_service.get_available_voltages(db, model_name)
        if voltages:
            print(f"✓ Voltages found for {model_name}: {voltages}")
        else:
            print(f"✗ No voltages found for {model_name}")
        
        # Test getting additional options
        print(f"\n--- Testing additional options for {model_name} ---")
        additional_options = product_service.get_additional_options(model_name)
        if additional_options:
            print(f"✓ Additional options found for {model_name}: {len(additional_options)} options")
            for opt in additional_options:
                print(f"  - {opt.get('name', 'Unknown')}: {opt.get('category', 'Unknown')}")
        else:
            print(f"✗ No additional options found for {model_name}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main() 