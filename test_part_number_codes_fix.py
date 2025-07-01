#!/usr/bin/env python3
"""
Test script to verify the part number generation fixes:
1. XSP for Extra Static Protection (was xsp)
2. SSTAG for Stainless Steel Tag
3. VR for Vibration Resistance
4. EPOX for Epoxy House
5. Fix for 3/4" diameter probe not triggering insulator material code incorrectly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService

def test_part_number_codes_fix():
    """Test the part number generation fixes."""
    db = SessionLocal()
    try:
        product_service = ProductService(db=db)
        config_service = ConfigurationService(db, product_service)
        
        print("=== TESTING PART NUMBER CODES FIX ===")
        
        # Start configuration
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
        
        # Test 1: Extra Static Protection (should be XSP)
        print("\n--- Test 1: Extra Static Protection ---")
        config_service.set_option("Extra Static Protection", "Yes")
        part_number = config_service.generate_model_number()
        print(f"With Extra Static Protection: {part_number}")
        assert "XSP" in part_number, f"Expected XSP in part number, got: {part_number}"
        print("✅ XSP code correctly added")
        
        # Test 2: Stainless Steel Tag (should be SSTAG)
        print("\n--- Test 2: Stainless Steel Tag ---")
        config_service.set_option("Stainless Steel Tag", "Yes")
        part_number = config_service.generate_model_number()
        print(f"With Stainless Steel Tag: {part_number}")
        assert "SSTAG" in part_number, f"Expected SSTAG in part number, got: {part_number}"
        print("✅ SSTAG code correctly added")
        
        # Test 3: Vibration Resistance (should be VR)
        print("\n--- Test 3: Vibration Resistance ---")
        config_service.set_option("Vibration Resistance", "Yes")
        part_number = config_service.generate_model_number()
        print(f"With Vibration Resistance: {part_number}")
        assert "VR" in part_number, f"Expected VR in part number, got: {part_number}"
        print("✅ VR code correctly added")
        
        # Test 4: Epoxy House (should be EPOX)
        print("\n--- Test 4: Epoxy House ---")
        config_service.set_option("Epoxy House", "Yes")
        part_number = config_service.generate_model_number()
        print(f"With Epoxy House: {part_number}")
        assert "EPOX" in part_number, f"Expected EPOX in part number, got: {part_number}"
        print("✅ EPOX code correctly added")
        
        # Test 5: 3/4" Diameter Probe (should be 3/4OD and NOT trigger insulator material)
        print("\n--- Test 5: 3/4\" Diameter Probe ---")
        # Start fresh configuration
        config_service.start_configuration(
            product_family_id=1,
            product_family_name="LS2000",
            base_product_info={"name": "LS2000", "id": 1, "base_length": 10}
        )
        config_service.set_option("Voltage", "115VAC")
        config_service.set_option("Material", "S")
        config_service.set_option("Probe Length", 10)
        
        # Add 3/4" diameter probe
        config_service.set_option('3/4" Diameter Probe', "Yes")
        part_number = config_service.generate_model_number()
        print(f"With 3/4\" Diameter Probe: {part_number}")
        assert "3/4OD" in part_number, f"Expected 3/4OD in part number, got: {part_number}"
        # Check that no insulator material code was added
        insulator_codes = ["TEFINS", "PEEKINS", "CERINS", "DELINS"]
        for code in insulator_codes:
            assert code not in part_number, f"Unexpected insulator code {code} in part number: {part_number}"
        print("✅ 3/4OD code correctly added, no insulator material code incorrectly added")
        
        # Test 6: 3/4" Diameter Probe + Teflon Insulator (both should be present)
        print("\n--- Test 6: 3/4\" Diameter Probe + Teflon Insulator ---")
        config_service.set_option("Insulator Material", "Teflon Upgrade")
        part_number = config_service.generate_model_number()
        print(f"With 3/4\" Diameter Probe + Teflon: {part_number}")
        assert "3/4OD" in part_number, f"Expected 3/4OD in part number, got: {part_number}"
        assert "TEFINS" in part_number, f"Expected TEFINS in part number, got: {part_number}"
        print("✅ Both 3/4OD and TEFINS codes correctly added")
        
        print("\n=== ALL TESTS PASSED ===")
        print("✅ Part number generation fixes working correctly!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_part_number_codes_fix() 