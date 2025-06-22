#!/usr/bin/env python3
"""
Debug script to investigate the $280 spare parts issue.
"""

import sys
import os
sys.path.append(os.path.abspath('.'))

from src.core.database import SessionLocal
from src.core.services.spare_part_service import SparePartService
from src.core.services.product_service import ProductService

def debug_spare_parts_issue():
    """Debug the spare parts pricing issue."""
    
    db = SessionLocal()
    
    try:
        print("=== DEBUGGING SPARE PARTS ISSUE ===")
        print()
        
        # Test 1: Check if any spare parts are being auto-selected
        print("1. Testing spare parts retrieval for different families:")
        
        test_families = ["LS2000", "LS2100", "LS6000", "LS7000", "LS8000", "FS10000"]
        
        for family_name in test_families:
            spare_parts = SparePartService.get_spare_parts_by_family(db, family_name)
            print(f"\n{family_name}: {len(spare_parts)} spare parts")
            
            total_value = 0
            for part in spare_parts:
                print(f"  - {part.part_number}: {part.name} (${part.price:.2f})")
                total_value += part.price
            
            if total_value > 0:
                print(f"  Total value of all spare parts: ${total_value:.2f}")
        
        # Test 2: Check if there's a specific $280 part
        print(f"\n2. Looking for $280 spare parts:")
        all_spare_parts = SparePartService.get_all_spare_parts(db)
        
        for part in all_spare_parts:
            if abs(part.price - 280.0) < 0.01:  # Within 1 cent
                print(f"  Found $280 part: {part.part_number} - {part.name} (Family: {part.product_family.name})")
        
        # Test 3: Check if any spare parts are being auto-selected in the UI
        print(f"\n3. Testing product service integration:")
        product_service = ProductService(db)
        
        for family_name in test_families[:3]:  # Test first 3 families
            print(f"\nTesting {family_name}:")
            
            # Get base product info
            base_product = product_service.get_base_product_for_family(db, family_name)
            if base_product:
                print(f"  Base price: ${base_product['base_price']:.2f}")
                
                # Get spare parts
                spare_parts = SparePartService.get_spare_parts_by_family(db, family_name)
                print(f"  Available spare parts: {len(spare_parts)}")
                
                # Calculate total spare parts value
                total_spare_value = sum(part.price for part in spare_parts)
                print(f"  Total spare parts value: ${total_spare_value:.2f}")
                
                # Check if any spare parts are $280
                for part in spare_parts:
                    if abs(part.price - 280.0) < 0.01:
                        print(f"  ⚠️  Found $280 spare part: {part.name}")
        
        print(f"\n=== DEBUG COMPLETE ===")
        
    except Exception as e:
        print(f"❌ Error during debug: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_spare_parts_issue() 