#!/usr/bin/env python3
"""
Debug script to investigate the $280 pricing issue.
"""

import sys
import os
sys.path.append(os.path.abspath('.'))

from src.core.database import SessionLocal
from src.core.services.spare_part_service import SparePartService
from src.core.services.product_service import ProductService

def debug_280_issue():
    """Debug the $280 pricing issue."""
    
    db = SessionLocal()
    
    try:
        print("=== DEBUGGING $280 ISSUE ===")
        print()
        
        # Test 1: Check if any spare parts are $280
        print("1. Looking for $280 spare parts:")
        all_spare_parts = SparePartService.get_all_spare_parts(db)
        
        for part in all_spare_parts:
            if abs(part.price - 280.0) < 0.01:  # Within 1 cent
                print(f"  Found $280 part: {part.part_number} - {part.name} (Family: {part.product_family.name})")
        
        # Test 2: Check if any spare parts are being auto-selected
        print(f"\n2. Checking if spare parts are being auto-selected:")
        
        # Simulate the pricing calculation logic
        selected_spare_parts = {}  # This should be empty
        
        spare_parts_total = 0.0
        if hasattr(selected_spare_parts, 'values'):
            spare_parts_total = sum(
                data['part'].price * data['quantity'] 
                for data in selected_spare_parts.values()
            )
        
        print(f"  selected_spare_parts: {selected_spare_parts}")
        print(f"  spare_parts_total: ${spare_parts_total:.2f}")
        
        # Test 3: Check if there's a default spare part being added
        print(f"\n3. Checking for default spare parts:")
        
        # Check if there's a default spare part in the database that might be auto-selected
        ls7000_parts = SparePartService.get_spare_parts_by_family(db, "LS7000")
        print(f"  LS7000 spare parts: {len(ls7000_parts)}")
        for part in ls7000_parts:
            print(f"    - {part.part_number}: {part.name} (${part.price:.2f})")
        
        # Test 4: Check the product service for any default behavior
        print(f"\n4. Checking product service for default behavior:")
        product_service = ProductService(db)
        
        # Get base product for LS7000
        base_product = product_service.get_base_product_for_family(db, "LS7000")
        if base_product:
            print(f"  LS7000 base price: ${base_product['base_price']:.2f}")
        
        # Test 5: Check if there's a default spare part in the UI initialization
        print(f"\n5. Checking UI initialization:")
        
        # Simulate the UI initialization
        selected_spare_parts = {}
        print(f"  Initial selected_spare_parts: {selected_spare_parts}")
        
        # Check if any spare parts are being added by default
        if hasattr(selected_spare_parts, 'values') and selected_spare_parts:
            print(f"  WARNING: selected_spare_parts is not empty!")
            for key, data in selected_spare_parts.items():
                print(f"    - {key}: {data['part'].name} (${data['part'].price:.2f})")
        else:
            print(f"  selected_spare_parts is empty (correct)")
        
        # Test 6: Check if there's a default spare part being added in the spare parts section
        print(f"\n6. Checking spare parts section creation:")
        
        # Simulate creating the spare parts section for LS7000
        from src.core.models.product_variant import ProductFamily
        ls7000_family = db.query(ProductFamily).filter(ProductFamily.name == "LS7000").first()
        if ls7000_family:
            print(f"  LS7000 family found: {ls7000_family.name}")
            
            # Get spare parts for LS7000
            spare_parts = SparePartService.get_spare_parts_by_family(db, "LS7000")
            print(f"  Spare parts for LS7000: {len(spare_parts)}")
            
            # Check if any of these are being auto-selected
            for part in spare_parts:
                print(f"    - {part.part_number}: {part.name} (${part.price:.2f})")
        
        # Test 7: Check if there's a default spare part being added in the browsing interface
        print(f"\n7. Checking browsing interface creation:")
        
        # Simulate creating the browsing interface
        all_spare_parts = SparePartService.get_all_spare_parts(db)
        spare_parts_by_family = {}
        for part in all_spare_parts:
            family_name = part.product_family.name
            if family_name not in spare_parts_by_family:
                spare_parts_by_family[family_name] = []
            spare_parts_by_family[family_name].append(part)
        
        print(f"  Total spare parts: {len(all_spare_parts)}")
        print(f"  Families with spare parts: {len(spare_parts_by_family)}")
        
        # Check if any spare parts are $280
        for family_name, parts in spare_parts_by_family.items():
            for part in parts:
                if abs(part.price - 280.0) < 0.01:
                    print(f"    WARNING: Found $280 part in {family_name}: {part.name}")
        
        print(f"\n=== DEBUG COMPLETE ===")
        
    except Exception as e:
        print(f"❌ Error during debug: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_280_issue() 