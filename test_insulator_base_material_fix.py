#!/usr/bin/env python3
"""
Test script to verify that insulator material codes are properly removed 
when switching back to base materials (e.g., S material for LS2000).
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService

def test_insulator_base_material_fix():
    """Test that insulator codes are removed when switching back to base materials."""
    db = SessionLocal()
    try:
        product_service = ProductService(db=db)
        config_service = ConfigurationService(db, product_service)
        
        print("=== TESTING INSULATOR BASE MATERIAL FIX ===")
        
        # Start configuration for LS2000
        config_service.start_configuration(
            product_family_id=1,
            product_family_name="LS2000",
            base_product_info={"name": "LS2000", "id": 1, "base_length": 10}
        )
        
        # Set basic options
        config_service.set_option("Voltage", "115VAC")
        config_service.set_option("Material", "S")
        config_service.set_option("Probe Length", 10)
        
        print(f"Basic part number: {config_service.generate_model_number()}")
        
        # Test 1: Add non-base insulator material (Teflon)
        print("\n--- Test 1: Add Teflon Insulator ---")
        config_service.set_option("Insulator Material", "Teflon Upgrade")
        part_number = config_service.generate_model_number()
        print(f"With Teflon Insulator: {part_number}")
        assert "TEFINS" in part_number, f"Expected TEFINS in part number, got: {part_number}"
        print("✅ TEFINS code correctly added")
        
        # Test 2: Switch back to base insulator material (S)
        print("\n--- Test 2: Switch back to base insulator (S) ---")
        config_service.set_option("Insulator Material", "S")
        part_number = config_service.generate_model_number()
        print(f"With base insulator (S): {part_number}")
        assert "TEFINS" not in part_number, f"Expected TEFINS to be removed from part number, got: {part_number}"
        print("✅ TEFINS code correctly removed when switching to base material")
        
        # Test 3: Switch to another non-base insulator (PEEK)
        print("\n--- Test 3: Switch to PEEK Insulator ---")
        config_service.set_option("Insulator Material", "PEEK")
        part_number = config_service.generate_model_number()
        print(f"With PEEK Insulator: {part_number}")
        assert "PEEKINS" in part_number, f"Expected PEEKINS in part number, got: {part_number}"
        print("✅ PEEKINS code correctly added")
        
        # Test 4: Switch back to base insulator material again
        print("\n--- Test 4: Switch back to base insulator (S) again ---")
        config_service.set_option("Insulator Material", "S")
        part_number = config_service.generate_model_number()
        print(f"With base insulator (S): {part_number}")
        assert "PEEKINS" not in part_number, f"Expected PEEKINS to be removed from part number, got: {part_number}"
        print("✅ PEEKINS code correctly removed when switching to base material")
        
        # Test 5: Test with "Standard" insulator material
        print("\n--- Test 5: Switch to Standard insulator ---")
        config_service.set_option("Insulator Material", "Standard")
        part_number = config_service.generate_model_number()
        print(f"With Standard Insulator: {part_number}")
        insulator_codes = ["TEFINS", "PEEKINS", "CERINS", "DELINS"]
        for code in insulator_codes:
            assert code not in part_number, f"Unexpected insulator code {code} in part number: {part_number}"
        print("✅ No insulator codes added for Standard material")
        
        # Test 6: Test with non-standard length + base material
        print("\n--- Test 6: Non-standard length with base material ---")
        config_service.set_option("Insulator Material", "S")
        config_service.set_option("Insulator Length", "15")
        part_number = config_service.generate_model_number()
        print(f"With base insulator (S) and non-standard length: {part_number}")
        insulator_codes = ["TEFINS", "PEEKINS", "CERINS", "DELINS"]
        for code in insulator_codes:
            assert code not in part_number, f"Unexpected insulator code {code} in part number: {part_number}"
        print("✅ No insulator codes added for base material even with non-standard length")
        
        print("\n=== ALL TESTS PASSED ===")
        print("✅ Insulator material base detection working correctly!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_insulator_base_material_fix() 