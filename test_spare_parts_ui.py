#!/usr/bin/env python3
"""
Test script to verify spare parts functionality in the UI.
"""

import sys
import os
sys.path.append(os.path.abspath('.'))

from src.core.database import SessionLocal
from src.core.services.spare_part_service import SparePartService
from src.core.services.product_service import ProductService

def test_spare_parts_functionality():
    """Test that spare parts are properly loaded and accessible."""
    
    db = SessionLocal()
    
    try:
        print("Testing Spare Parts Functionality")
        print("=" * 50)
        
        # Test 1: Check if spare parts exist in database
        all_spare_parts = SparePartService.get_all_spare_parts(db)
        print(f"Total spare parts in database: {len(all_spare_parts)}")
        
        if not all_spare_parts:
            print("❌ No spare parts found in database!")
            return
        
        # Test 2: Check spare parts by product family
        test_families = ["LS2000", "LS2100", "LS6000", "FS10000"]
        
        for family_name in test_families:
            spare_parts = SparePartService.get_spare_parts_by_family(db, family_name)
            print(f"\n{family_name}: {len(spare_parts)} spare parts")
            
            for part in spare_parts[:3]:  # Show first 3 parts
                print(f"  - {part.part_number}: {part.name} (${part.price:.2f})")
            
            if len(spare_parts) > 3:
                print(f"  ... and {len(spare_parts) - 3} more")
        
        # Test 3: Check categories
        print(f"\nSpare Parts by Category:")
        categories = {}
        for part in all_spare_parts:
            category = part.category if part.category else "Uncategorized"
            categories[category] = categories.get(category, 0) + 1
        
        for category, count in sorted(categories.items()):
            print(f"  {category}: {count} parts")
        
        # Test 4: Test product service integration
        product_service = ProductService(db)
        families = product_service.get_product_families(db)
        
        print(f"\nProduct Families with Spare Parts:")
        for family in families[:5]:  # Test first 5 families
            family_name = family['name']
            spare_parts = SparePartService.get_spare_parts_by_family(db, family_name)
            if spare_parts:
                print(f"  {family_name}: {len(spare_parts)} spare parts available")
        
        print(f"\n✅ Spare parts functionality test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error testing spare parts functionality: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_spare_parts_functionality() 