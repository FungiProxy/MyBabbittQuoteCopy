#!/usr/bin/env python3
"""
Debug script to check LS7000/2 and LS8000/2 issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.models.product_variant import ProductFamily

def debug_ls7000_2_issue():
    """Debug the LS7000/2 and LS8000/2 loading issue"""
    print("=== DEBUGGING LS7000/2 AND LS8000/2 ISSUE ===\n")
    
    db = SessionLocal()
    product_service = ProductService(db)
    
    try:
        # 1. Check if the families exist in the database
        print("1. Checking if families exist in database:")
        families = db.query(ProductFamily).all()
        ls7000_2_found = False
        ls8000_2_found = False
        
        for family in families:
            print(f"  - {family.name} (ID: {family.id})")
            if family.name == "LS7000/2":
                ls7000_2_found = True
            elif family.name == "LS8000/2":
                ls8000_2_found = True
        
        print(f"\n  LS7000/2 found: {ls7000_2_found}")
        print(f"  LS8000/2 found: {ls8000_2_found}")
        
        # 2. Check what get_product_families returns
        print("\n2. Checking get_product_families output:")
        product_families = product_service.get_product_families(db)
        print(f"  Total families returned: {len(product_families)}")
        
        ls7000_2_in_list = False
        ls8000_2_in_list = False
        
        for family in product_families:
            print(f"  - {family.get('name')} (ID: {family.get('id')})")
            if family.get('name') == "LS7000/2":
                ls7000_2_in_list = True
            elif family.get('name') == "LS8000/2":
                ls8000_2_in_list = True
        
        print(f"\n  LS7000/2 in product list: {ls7000_2_in_list}")
        print(f"  LS8000/2 in product list: {ls8000_2_in_list}")
        
        # 3. Test getting base product for these families
        print("\n3. Testing base product retrieval:")
        
        for model_name in ["LS7000/2", "LS8000/2"]:
            print(f"\n  Testing {model_name}:")
            try:
                base_product = product_service.get_base_product_for_family(db, model_name)
                if base_product:
                    print(f"    ✓ Base product found: {base_product}")
                else:
                    print(f"    ✗ No base product found")
            except Exception as e:
                print(f"    ✗ Error getting base product: {e}")
        
        # 4. Test getting materials for these families
        print("\n4. Testing material retrieval:")
        
        for model_name in ["LS7000/2", "LS8000/2"]:
            print(f"\n  Testing {model_name}:")
            try:
                materials = product_service.get_available_materials_for_product(db, model_name)
                if materials:
                    print(f"    ✓ Materials found: {len(materials)} options")
                    for mat in materials:
                        print(f"      - {mat.get('name', 'Unknown')}: {mat.get('choices', [])}")
                else:
                    print(f"    ✗ No materials found")
            except Exception as e:
                print(f"    ✗ Error getting materials: {e}")
        
        # 5. Test getting voltages for these families
        print("\n5. Testing voltage retrieval:")
        
        for model_name in ["LS7000/2", "LS8000/2"]:
            print(f"\n  Testing {model_name}:")
            try:
                voltages = product_service.get_available_voltages(db, model_name)
                if voltages:
                    print(f"    ✓ Voltages found: {voltages}")
                else:
                    print(f"    ✗ No voltages found")
            except Exception as e:
                print(f"    ✗ Error getting voltages: {e}")
        
    except Exception as e:
        print(f"Error in debug: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()
    
    print("\n=== DEBUG COMPLETE ===")

if __name__ == "__main__":
    debug_ls7000_2_issue() 